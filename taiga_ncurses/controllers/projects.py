# -*- coding: utf-8 -*-

"""
taiga_ncurses.controllers.projects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import functools

from taiga_ncurses.config import settings
from taiga_ncurses.ui import signals

from . import base

from .backlog import ProjectBacklogSubController
from .milestones import ProjectMilestoneSubController
from .issues import ProjectIssuesSubController
from .wiki import ProjectWikiSubController


class ProjectsController(base.Controller):
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


class ProjectDetailController(base.Controller):
    def __init__(self, view, executor, state_machine):
        self.view = view
        self.executor = executor
        self.state_machine = state_machine

        # Subcontrollers
        self.backlog = ProjectBacklogSubController(self.view.backlog, executor, state_machine)
        self.sprint = ProjectMilestoneSubController(self.view.sprint, executor, state_machine)
        self.issues = ProjectIssuesSubController(self.view.issues, executor, state_machine)
        self.wiki = ProjectWikiSubController(self.view.wiki, executor, state_machine)
        self.admin = ProjectAdminSubController(self.view.backlog, executor, state_machine)

        self.subcontroller = self.backlog
        self.subcontroller.load()

    def handle(self, key):
        if key == settings.data.main.keys.backlog:
            self.view.backlog_view()
            self.subcontroller = self.backlog
            self.subcontroller.load()
        elif key == settings.data.main.keys.milestone:
            self.view.sprint_view()
            self.subcontroller = self.sprint
            self.subcontroller.load()
        elif key == settings.data.main.keys.issues:
            self.view.issues_view()
            self.subcontroller = self.issues
            self.subcontroller.load()
        elif key == settings.data.main.keys.wiki:
            self.view.wiki_view()
            self.subcontroller = self.wiki
            self.subcontroller.load()
        elif key == settings.data.main.keys.admin:
            self.view.admin_view()
            self.subcontroller = self.admin
        elif key == settings.data.main.keys.projects:
            self.state_machine.projects()
        else:
            self.subcontroller.handle(key)


class ProjectAdminSubController(base.Controller):
    def __init__(self, view, executor, state_machine):
        self.view = view
        self.executor = executor
        self.state_machine = state_machine
