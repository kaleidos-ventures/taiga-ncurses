# -*- coding: utf-8 -*-

"""
gmncurses.controllers
~~~~~~~~~~~~~~~~~~~~~
"""

from concurrent.futures import wait
import functools

from .config import ProjectKeys, ProjectBacklogKeys, ProjectSprintKeys, ProjectIssuesKeys
from .ui import signals

import gmncurses.data


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

        signals.connect(self.view.user_story_form.cancel_button, "click",
                lambda _: self.cancel_user_story_form())
        signals.connect(self.view.user_story_form.save_button, "click",
                lambda _: self.handler_create_user_story_request())

    def handle(self, key):
        if key == ProjectBacklogKeys.CREATE_USER_STORY:
            self.new_user_story_form()
        elif key == ProjectBacklogKeys.RELOAD:
            self.load()
        elif key == ProjectBacklogKeys.US_UP:
            self.move_current_us_up()
        elif key == ProjectBacklogKeys.US_DOWN:
            self.move_current_us_down()
        elif key == ProjectBacklogKeys.UPDATE_USER_STORIES_ORDER:
            self.update_user_stories_order()
        return super().handle(key)

    def load(self):
        self.state_machine.transition(self.state_machine.PROJECT_BACKLOG)

        self.view.notifier.info_msg("Fetching Stats and User stories")

        project_stats_f = self.executor.project_stats(self.view.project)
        project_stats_f.add_done_callback(self.handle_project_stats)

        user_stories_f = self.executor.unassigned_user_stories(self.view.project)
        user_stories_f.add_done_callback(self.handle_user_stories)

        futures = (project_stats_f, user_stories_f)
        futures_completed_f = self.executor.pool.submit(lambda : wait(futures, 10))
        futures_completed_f.add_done_callback(functools.partial(self.when_backlog_info_fetched,
                                                                info_msg="Project stats and user stories "
                                                                         "fetched",
                                                                error_msg="Failed to fetch project data"))

    def new_user_story_form(self):
        self.view.new_user_story_form()

    def cancel_user_story_form(self):
        self.view.user_stories_list()

    def move_current_us_up(self):
        current_focus = self.user_stories.index(self.view.user_stories.widget.get_focus().user_story)

        if current_focus > 0 and len(self.user_stories) > 2:
            current_us = self.user_stories[current_focus]
            self.user_stories[current_focus] = self.user_stories[current_focus - 1]
            self.user_stories[current_focus - 1] = current_us

            self.view.notifier.info_msg("Moved User story #{} up".format(current_us["ref"]))

            self.view.user_stories.populate(self.user_stories, self.project_stats, set_focus=current_us)

    def move_current_us_down(self):
        current_focus = self.user_stories.index(self.view.user_stories.widget.get_focus().user_story)

        if current_focus < len(self.user_stories) - 1 and len(self.user_stories) > 2:
            current_us = self.user_stories[current_focus]
            self.user_stories[current_focus] = self.user_stories[current_focus + 1]
            self.user_stories[current_focus + 1] = current_us

            self.view.notifier.info_msg("Moved User story #{} down".format(current_us["ref"]))

            self.view.user_stories.populate(self.user_stories, self.project_stats, set_focus=current_us)

    def update_user_stories_order(self):
        uss_post_f = self.executor.update_user_stories_order(self.user_stories, self.view.project)
        uss_post_f.add_done_callback(self.handler_update_user_stories_order_response)

    def handle_project_stats(self, future):
        self.project_stats = future.result()

    def handle_user_stories(self, future):
        self.user_stories = future.result()

    def when_backlog_info_fetched(self, future_with_results, info_msg=None, error_msg=None):
        done, not_done = future_with_results.result()

        if len(done) == 2:
            # FIXME TODO: Moved to handle_project_stats and fixed populate method tu update the content
            #             of the main widget instead of replace the widget
            if self.project_stats is not None:
                self.view.stats.populate(self.project_stats)

            self.view.user_stories.populate(self.user_stories, self.project_stats)
            if info_msg:
                self.view.notifier.info_msg(info_msg) #
            self.state_machine.refresh()
        else:
            # TODO retry failed operationsi
            if error_msg:
                self.view.notifier.error_msg(error_msg)

    def handler_create_user_story_request(self):
        data = self.view.get_user_story_form_data()

        if not data.get("subject", None):
            self.view.notifier.error_msg("Subject is required")
        else:
            us_post_f = self.executor.create_user_story(data)
            us_post_f.add_done_callback(self.handler_create_user_story_response)

    def handler_create_user_story_response(self, future):
        response = future.result()

        if response is None:
            self.view.notifier.error_msg("Create error")
        else:
            self.view.notifier.info_msg("Create succesful!")
            self.view.user_stories_list()

            project_stats_f = self.executor.project_stats(self.view.project)
            project_stats_f.add_done_callback(self.handle_project_stats)

            user_stories_f = self.executor.unassigned_user_stories(self.view.project)
            user_stories_f.add_done_callback(self.handle_user_stories)

            futures = (project_stats_f, user_stories_f)
            futures_completed_f = self.executor.pool.submit(lambda : wait(futures, 10))
            futures_completed_f.add_done_callback(functools.partial(self.when_backlog_info_fetched))

    def handler_update_user_stories_order_response(self, future):
        response = future.result()

        if response is None:
            self.view.notifier.error_msg("Error moving user_story")

            user_stories_f = self.executor.unassigned_user_stories(self.view.project)
            user_stories_f.add_done_callback(self.handle_user_stories)
        else:
            self.view.notifier.info_msg("Save  user stories")

            project_stats_f = self.executor.project_stats(self.view.project)
            project_stats_f.add_done_callback(self.handle_project_stats)

            user_stories_f = self.executor.unassigned_user_stories(self.view.project)
            user_stories_f.add_done_callback(self.handle_user_stories)

            futures = (project_stats_f, user_stories_f)
            futures_completed_f = self.executor.pool.submit(lambda : wait(futures, 10))
            futures_completed_f.add_done_callback(functools.partial(self.when_backlog_info_fetched))


class ProjectSprintSubController(Controller):
    def __init__(self, view, executor, state_machine):
        self.view = view
        self.executor = executor
        self.state_machine = state_machine

    def handle(self, key):
        if key == ProjectSprintKeys.RELOAD:
            self.load()
        return super().handle(key)

    def load(self):
        self.state_machine.transition(self.state_machine.PROJECT_SPRINT)

        self.view.notifier.info_msg("Fetching Stats and User stories")

        res = gmncurses.data.current_sprint_id(self.view.project)

        milestone_stats_f = self.executor.milestone_stats(res, self.view.project)
        milestone_stats_f.add_done_callback(self.handle_milestone_stats)

        user_stories_f = self.executor.user_stories(res, self.view.project)
        user_stories_f.add_done_callback(self.handle_user_stories)

        milestone_tasks_f = self.executor.milestone_tasks(res, self.view.project)
        milestone_tasks_f.add_done_callback(self.handle_milestone_tasks)

        futures = (milestone_tasks_f, user_stories_f)
        futures_completed_f = self.executor.pool.submit(lambda : wait(futures, 10))
        futures_completed_f.add_done_callback(self.user_stories_info_fetched)

    def handle_milestone_stats(self, future):
        self.milestone_stats = future.result()
        if self.milestone_stats is not None:
            self.view.stats.populate(self.milestone_stats)
            self.state_machine.refresh()

    def handle_user_stories(self, future):
        self.user_stories = future.result()
        #if self.user_stories is not None:
            #self.view.user_stories_list.populate(self.user_stories)
            #self.state_machine.refresh()

    def handle_milestone_tasks(self, future):
        self.milestone_tasks = future.result()

    def user_stories_info_fetched(self, future_with_results):
        done, not_done = future_with_results.result()
        if len(done) == 2:
            self.view.user_stories_list.populate(self.user_stories, self.milestone_tasks)
            self.view.notifier.info_msg("user stories and tasks fetched")
            self.state_machine.refresh()
        else:
            # TODO retry failed operations
            self.view.notifier.error_msg("Failed to fetch milestone data")


class ProjectIssuesSubController(Controller):
    def __init__(self, view, executor, state_machine):
        self.view = view
        self.executor = executor
        self.state_machine = state_machine

    def handle(self, key):
        if key == ProjectIssuesKeys.RELOAD:
            self.load()
        return super().handle(key)


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

            signals.connect(self.view.issues.header.issue_button, "click",
                    functools.partial(self.order_by, "issue"))

            signals.connect(self.view.issues.header.status_button, "click",
                    functools.partial(self.order_by, "status"))

            signals.connect(self.view.issues.header.priority_button, "click",
                    functools.partial(self.order_by, "priority"))

            signals.connect(self.view.issues.header.severity_buttton, "click",
                    functools.partial(self.order_by, "severity"))

            signals.connect(self.view.issues.header.assigned_to_button, "click",
                    functools.partial(self.order_by, "assigned_to"))

            self.state_machine.refresh()

    def when_issues_info_fetched(self, future_with_results):
        done, not_done = future_with_results.result()
        if len(done) == 2:
            self.view.notifier.info_msg("Stats and issues fetched")
            self.state_machine.refresh()
        else:
            # TODO retry failed operations
            self.view.notifier.error_msg("Failed to fetch issues data")

    def order_by(self, param, button):
        self.view.notifier.info_msg("Ordered issues by {}".format(param))
        issues_f = self.executor.issues(self.view.project, order_by=[param])
        issues_f.add_done_callback(self.handle_refresh_issues)

    def handle_refresh_issues(self, future):
        self.issues = future.result()
        if self.issues is not None:
            self.view.issues.populate(self.issues)
            self.state_machine.refresh()


class ProjectWikiSubController(Controller):
    def __init__(self, view, executor, state_machine):
        self.view = view
        self.executor = executor
        self.state_machine = state_machine

    def load(self):
        self.state_machine.transition(self.state_machine.PROJECT_WIKI)

        self.view.notifier.info_msg("Fetching Wiki")

        wiki_pages_f = self.executor.wiki_pages(self.view.project)
        wiki_pages_f.add_done_callback(self.handle_wiki_pages)

        futures = (wiki_pages_f,)
        futures_completed_f = self.executor.pool.submit(lambda : wait(futures, 10))
        futures_completed_f.add_done_callback(self.when_wiki_pages_fetched)

    def handle_wiki_pages(self, future):
        self.wiki_pages = future.result()
        if self.wiki_pages is not None:
            if len(self.wiki_pages) > 0:
                self.view.wiki_page.populate(self.wiki_pages[0])
            self.state_machine.refresh()

    def when_wiki_pages_fetched(self, future_with_results):
        done, not_done = future_with_results.result()
        if len(done) == 1:
            self.view.notifier.info_msg("Wiki pages fetched")
            self.state_machine.refresh()
        else:
            # TODO retry failed operations
            self.view.notifier.error_msg("Failed to fetch wiki data")


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
        self.sprint = ProjectSprintSubController(self.view.sprint, executor, state_machine)
        self.issues = ProjectIssuesSubController(self.view.issues, executor, state_machine)
        self.wiki = ProjectWikiSubController(self.view.wiki, executor, state_machine)
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
            self.subcontroller.load()
        elif key == ProjectKeys.ISSUES:
            self.view.issues_view()
            self.subcontroller = self.issues
            self.subcontroller.load()
        elif key == ProjectKeys.WIKI:
            self.view.wiki_view()
            self.subcontroller = self.wiki
            self.subcontroller.load()
        elif key == ProjectKeys.ADMIN:
            self.view.admin_view()
            self.subcontroller = self.admin
        else:
            self.subcontroller.handle(key)
