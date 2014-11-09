# -*- coding: utf-8 -*-

"""
taiga_ncurses.core
~~~~~~~~~~~~~~~~~~
"""

import functools
from concurrent.futures import wait

import urwid

from taiga_ncurses.ui import views
from taiga_ncurses import controllers
from taiga_ncurses.config import settings


class TaigaCore:
    def __init__(self, executor, settings, authenticated=False, draw=True):
        self.executor = executor
        self.settings = settings
        self.draw = draw

        if authenticated:
            self.state_machine = StateMachine(self, state=StateMachine.PROJECTS)
            self.controller = self._build_projects_controller()
        else:
            self.state_machine = StateMachine(self, state=StateMachine.LOGIN)
            self.controller = self._build_login_controller()

        # Main Loop
        self.loop = urwid.MainLoop(self.controller.view.widget,
                                   palette=self.settings.palette,
                                   unhandled_input=self.key_handler,
                                   handle_mouse=True,
                                   pop_ups=True)

    def run(self):
        self.loop.run()

    def key_handler(self, key):
        if key == settings.data.main.keys.quit:
            self.settings.save()
            raise urwid.ExitMainLoop
        elif key == settings.data.main.keys.debug:
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
        self.controller = self._build_project_controller(project)
        self.transition()

    def transition(self):
        if self.draw:
            self.loop.widget = self.controller.view.widget
            self.loop.widget._invalidate()
            self.loop.draw_screen()

    def set_auth_config(self, auth_data):
        self.settings.data.auth.token = auth_data["auth_token"]

    def _build_login_controller(self):
        login_view = views.auth.LoginView('username', 'password')
        login_controller = controllers.auth.LoginController(login_view,
                                                            self.executor,
                                                            self.state_machine)
        return login_controller

    def _build_projects_controller(self):
        projects_view = views.projects.ProjectsView()
        projects_controller = controllers.projects.ProjectsController(projects_view,
                                                                      self.executor,
                                                                      self.state_machine)
        return projects_controller

    def _build_project_controller(self, project):
        project_view = views.projects.ProjectDetailView(project)
        project_controller = controllers.projects.ProjectDetailController(project_view,
                                                                          self.executor,
                                                                          self.state_machine)
        return project_controller


class StateMeta(type):
    def __new__(cls, clsname, bases, dct):
        state_attrs = [k for k in dct if k.isupper()]
        state_set = {dct[s] for s in state_attrs}
        assert len(state_attrs) == len(state_set), "State attributes must be unique"
        dct["STATES"] = state_set
        return super().__new__(cls, clsname, bases, dct)


class StateMachine(metaclass=StateMeta):
    LOGIN = 0
    PROJECTS = 1
    PROJECT_BACKLOG = 2
    PROJECT_MILESTONES = 3
    PROJECT_ISSUES = 4
    PROJECT_WIKI = 5
    PROJECT_ADMIN = 6

    def __init__(self, core, state):
        self._core = core
        self.state = state

    def logged_in(self, auth_data):
        self._core.set_auth_config(auth_data)
        self._core.projects_view()

    def projects(self):
        self._core.projects_view()

    def project_detail(self, project):
        self._core.project_view(project)

    def transition(self, state):
        assert state in self.STATES, "{0} is not a valid state".format(state)
        self.state = state
        self.refresh()

    def refresh(self):
        self._core.transition()
