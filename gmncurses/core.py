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
    def __init__(self, client):
        self.client = client
        self.executor = Executor(client)
        self.sm = StateMachine(self)

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
            raise urwid.ExitMainLoop
        elif key == Keys.DEBUG:
            self.debug()
        else:
            return self.controller.handle(key)

    def debug(self):
        self.loop.screen.stop()
        import ipdb; ipdb.set_trace()
        self.loop.screen.start()

    def _build_login_controller(self):
        login_view = views.LoginView('username', 'password')
        login_controller = controllers.LoginController(login_view, self.executor, self.sm)
        return login_controller

    def login_view(self):
        pass

    def _build_project_controller(self):
        projects = self.client.get_projects()
        projects_view = views.ProjectsView(projects)
        projects_controller = controllers.ProjectsController(self, projects_view)
        return projects_controller

    def projects_view(self):
        self.controller = self._build_project_controller()
        self.loop.widget = self.controller.view.widget
        self.loop.draw_screen()

    def save_auth_token(self, auth_data):
        #self.debug()
        pass


class StateMachine(object):
    LOGIN = 0
    PROJECTS = 1
    PROJECT_USERSTORIES = 2
    # TODO

    def __init__(self, core, state=LOGIN):
        self._core = core
        self._state = state

    def logged_in(self, auth_data):
        self._state = self.PROJECTS
        self._core.save_auth_token(auth_data)
        self._core.projects_view()
