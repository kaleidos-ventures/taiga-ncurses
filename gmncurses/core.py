# -*- coding: utf-8 -*-

"""
gmncurses.core
~~~~~~~~~~~~~~
"""

import functools

import urwid

from gmncurses.ui import views
from gmncurses import controllers
from gmncurses.config import Keys, PALETTE
from gmncurses.executor import Executor


class GreenMineCore(object):
    def __init__(self, client, configuration):
        self.client = client
        self.configuration = configuration

        self.executor = Executor(client)

        if client.is_authenticated:
            self.state_machine = StateMachine(self, state=StateMachine.PROJECTS)
            self.controller = self._build_projects_controller()
        else:
            self.state_machine = StateMachine(self, state=StateMachine.LOGIN)
            self.controller = self._build_login_controller()

        # Main Loop
        self.loop = urwid.MainLoop(self.controller.view.widget,
                                   palette=PALETTE,
                                   unhandled_input=self.key_handler,
                                   handle_mouse=True)

    def run(self):
        self.loop.run()

    def key_handler(self, key):
        if key == Keys.QUIT:
            self.configuration.save()
            raise urwid.ExitMainLoop
        elif key == Keys.DEBUG:
            self.debug()
        else:
            return self.controller.handle(key)

    def debug(self):
        self.loop.screen.stop()
        import ipdb; ipdb.set_trace()
        self.loop.screen.start()

    def login_view(self):
        pass

    def projects_view(self):
        self.controller = self._build_projects_controller()
        self.transition()

    def project_view(self, project):
        project = self.client.get_project(id=project["id"])
        project_stats = self.client.get_project_stats(id=project["id"])
        self.controller = self._build_project_controller(project, project_stats)
        self.transition()

    def transition(self):
        self.loop.widget = self.controller.view.widget
        self.loop.draw_screen()

    def set_auth_config(self, auth_data):
        self.configuration.config_dict["auth"] = {}
        self.configuration.config_dict["auth"]["token"] = auth_data["auth_token"]

    def _build_login_controller(self):
        login_view = views.LoginView('username', 'password')
        login_controller = controllers.LoginController(login_view,
                self.executor, self.state_machine)
        return login_controller

    def _build_projects_controller(self):
        projects = self.client.get_projects()
        projects_view = views.ProjectsView(projects)
        projects_controller = controllers.ProjectsController(projects_view,
                                                             self.executor,
                                                             self.state_machine)
        return projects_controller

    def _build_project_controller(self, project, project_stats):
        project_view = views.ProjectDetailView(project, project_stats)
        project_controller = controllers.ProjectDetailController(project_view,
                                                                 self.executor,
                                                                 self.state_machine)
        return project_controller

class StateMachine(object):
    LOGIN = 0
    PROJECTS = 1
    PROJECT_DETAIL = 2
    PROJECT_DETAIL_BACKLOG = 3
    # TODO

    def __init__(self, core, state):
        self._core = core
        self.state = state

    def logged_in(self, auth_data):
        self.state = self.PROJECTS
        self._core.set_auth_config(auth_data)
        self._core.projects_view()

    def project_detail(self, project_name):
        self.state = self.PROJECT_DETAIL
        self._core.project_view(project_name)

    def project_backlog(self):
        self.state = self.PROJECT_DETAIL_BACKLOG
        self._core.transition()
