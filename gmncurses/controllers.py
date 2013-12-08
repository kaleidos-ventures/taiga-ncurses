# -*- coding: utf-8 -*-

"""
gmncurses.controllers
~~~~~~~~~~~~~~~~~~~~~
"""

from concurrent.futures import wait
import functools

from .config import ProjectKeys
from .ui import signals


class Controller(object):
    view = None

    def handle(self, key):
        return key


class LoginController(Controller):
    def __init__(self, view, executor, state_machine):
        self.view = view
        self.executor = executor
        self.state_machine = state_machine

        signals.connect(self.view.login_button, "click", lambda _: self.handle_login_request())

    def handle_login_request(self):
        self.view.notifier.clear_msg()

        username = self.view.username
        password = self.view.password
        if not username or not password:
            self.view.notifier.error_msg("Enter your username and password")
            return

        logged_in_f = self.executor.login(username, password)
        logged_in_f.add_done_callback(self.handle_login_response)

    def handle_login_response(self, future):
        response = future.result()
        if response is None:
            self.view.notifier.error_msg("Login error")
        else:
            self.view.notifier.info_msg("Login succesful!")
            self.state_machine.logged_in(response)


class ProjectsController(Controller):
    def __init__(self, view, executor, state_machine):
        self.view = view
        self.executor = executor
        self.state_machine = state_machine

        projects_f = self.executor.projects()
        projects_f.add_done_callback(self.handle_projects_response)

    def handle_projects_response(self, future):
        projects = future.result()
        if projects is None:
            return # FIXME

        self.view.populate(projects)
        for b, p in zip(self.view.project_buttons, self.view.projects):
            signals.connect(b, "click", functools.partial(self.select_project, p))

        self.state_machine.transition(self.state_machine.PROJECTS)


    def select_project(self, project, project_button):
        self.view.notifier.info_msg("Fetching info of project: {}".format(project["name"]))
        project_fetch_f = self.executor.project_detail(project)
        project_fetch_f.add_done_callback(self.handle_project_response)

    def handle_project_response(self, future):
        project = future.result()
        if project is None:
            self.view.notifier.error_msg("Failed to fetch info of project")
        else:
            self.state_machine.project_detail(project)


class ProjectBacklogSubController(Controller):
    def __init__(self, view, executor, state_machine):
        self.view = view
        self.executor = executor
        self.state_machine = state_machine

    def load(self):
        self.state_machine.transition(self.state_machine.PROJECT_BACKLOG)

        self.view.notifier.info_msg("Fetching Stats and User stories")

        project_stats_f = self.executor.project_stats(self.view.project)
        project_stats_f.add_done_callback(self.handle_project_stats)

        user_stories_f = self.executor.unassigned_user_stories(self.view.project)
        user_stories_f.add_done_callback(self.handle_user_stories)

        futures = (project_stats_f, user_stories_f)
        futures_completed_f = self.executor.pool.submit(lambda : wait(futures, 10))
        futures_completed_f.add_done_callback(self.when_backlog_info_fetched)

    def handle_project_stats(self, future):
        self.project_stats = future.result()
        if self.project_stats is not None:
            self.view.stats.populate(self.project_stats)
            self.state_machine.refresh()

    def handle_user_stories(self, future):
        self.user_stories = future.result()

    def when_backlog_info_fetched(self, future_with_results):
        done, not_done = future_with_results.result()
        if len(done) == 2:
            self.view.user_stories.populate(self.user_stories, self.project_stats)
            self.view.notifier.info_msg("Project stats and user stories fetched")
            self.state_machine.refresh()
        else:
            # TODO retry failed operations
            self.view.notifier.error_msg("Failed to fetch project data")


class ProjectIssuesSubController(Controller):
    def __init__(self, view, executor, state_machine):
        self.view = view
        self.executor = executor
        self.state_machine = state_machine

    def load(self):
        self.state_machine.transition(self.state_machine.PROJECT_ISSUES)

        self.view.notifier.info_msg("Fetching Stats and Issues")

        issues_stats_f = self.executor.project_issues_stats(self.view.project)
        issues_stats_f.add_done_callback(self.handle_issues_stats)

        issues_f = self.executor.issues(self.view.project)
        issues_f.add_done_callback(self.handle_issues)

        futures = (issues_stats_f, issues_f)
        futures_completed_f = self.executor.pool.submit(lambda : wait(futures, 10))
        futures_completed_f.add_done_callback(self.when_issues_info_fetched)

    def handle_issues_stats(self, future):
        self.issues_stats = future.result()
        if self.issues_stats is not None:
            self.view.stats.populate(self.issues_stats)
            self.state_machine.refresh()

    def handle_issues(self, future):
        self.issues = future.result()
        if self.issues is not None:
            self.view.issues.populate(self.issues)
            self.state_machine.refresh()

    def when_issues_info_fetched(self, future_with_results):
        done, not_done = future_with_results.result()
        if len(done) == 2:
            self.view.notifier.info_msg("Stats and issues fetched")
            self.state_machine.refresh()
        else:
            # TODO retry failed operations
            self.view.notifier.error_msg("Failed to fetch issues data")


class ProjectSubController(Controller):
    def __init__(self, view, executor, state_machine):
        self.view = view
        self.executor = executor
        self.state_machine = state_machine


class ProjectDetailController(Controller):
    def __init__(self, view, executor, state_machine):
        self.view = view
        self.executor = executor
        self.state_machine = state_machine

        # Subcontrollers
        self.backlog = ProjectBacklogSubController(self.view.backlog, executor, state_machine)
        self.sprint = ProjectSubController(self.view.backlog, executor, state_machine)
        self.issues = ProjectIssuesSubController(self.view.issues, executor, state_machine)
        self.wiki = ProjectSubController(self.view.backlog, executor, state_machine)
        self.admin = ProjectSubController(self.view.backlog, executor, state_machine)

        self.subcontroller = self.backlog
        self.subcontroller.load()

    def handle(self, key):
        if key == ProjectKeys.BACKLOG:
            self.view.backlog_view()
            self.subcontroller = self.backlog
            self.subcontroller.load()
        elif key == ProjectKeys.SPRINT:
            self.view.sprint_view()
            self.subcontroller = self.sprint
        elif key == ProjectKeys.ISSUES:
            self.view.issues_view()
            self.subcontroller = self.issues
            self.subcontroller.load()
        elif key == ProjectKeys.WIKI:
            self.view.wiki_view()
            self.subcontroller = self.wiki
        elif key == ProjectKeys.ADMIN:
            self.view.admin_view()
            self.subcontroller = self.admin
        else:
            return self.subcontroller.handle(key)
