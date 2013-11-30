# -*- coding: utf-8 -*-

"""
gmncurses.controllers
~~~~~~~~~~~~~~~~~~~~~
"""

import functools

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
        if response:
            self.view.notifier.info_msg("Login succesful!")
            self.state_machine.logged_in(response)
        else:
            self.view.notifier.error_msg("Login error")


class ProjectsController(Controller):
    def __init__(self, view, state_machine):
        self.view = view
        self.state_machine = state_machine

        for b, p in zip(self.view.project_buttons, self.view.projects):
            signals.connect(b, "click", functools.partial(self.select_project, p))

    def select_project(self, project, project_button):
        self.state_machine.project_detail(project)


class ProjectDetailController(Controller):
    def __init__(self, view, state_machine):
        self.view = view
        self.state_machine = state_machine

