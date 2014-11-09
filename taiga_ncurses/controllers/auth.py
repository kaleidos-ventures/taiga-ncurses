# -*- coding: utf-8 -*-

"""
taiga_ncurses.controllers.auth
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from taiga_ncurses.ui import signals

from . import base


class LoginController(base.Controller):
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
            self.state_machine.refresh()
        else:
            self.view.notifier.info_msg("Login succesful!")
            self.state_machine.logged_in(response)
