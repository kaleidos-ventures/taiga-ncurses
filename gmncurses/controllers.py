# -*- coding: utf-8 -*-

"""
gmncurses.controllers
~~~~~~~~~~~~~~~~~~~~~
"""

from .ui import signals


class Controller(object):
    view = None

    def handle(self, key):
        return key


class LoginController(Controller):
    def __init__(self, loop, view, client):
        self.loop = loop
        self.view = view
        self.client = client

        signals.connect(self.view.login_button, 'click', lambda _: self.handle_login())

    def handle_login(self):
        self.view.notifier.clear_msg()
        user = self.view.username
        password = self.view.password

        if not user or not password:
            self.view.notifier.error_msg('Enter your username and password')
            return

        try:
            logged_in = self.client.login(user, password)
        except Exception as e:
            self.view.notifier.error_msg(e.args[0])
            return

        if logged_in:
            self.view.notifier.info_msg("Login succesful!")
            auth_token = logged_in.get("auth_token")
            self.loop.save_auth_token(auth_token)
            self.loop.projects_view()
        else:
            self.view.notifier.error_msg(self.client.last_error["detail"])


class ProjectsController(Controller):
    def __init__(self, loop, view):
        self.loop = loop
        self.view = view
