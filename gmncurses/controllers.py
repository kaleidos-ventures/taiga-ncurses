"""
controllers
~~~~~~~~~~~

"""

import urwid


class Controller(object):
    view = None

    def handle(self, key):
        return key


class LoginController(Controller):
    def __init__(self, loop, view, client):
        self.loop = loop
        self.view = view
        self.client = client

        urwid.connect_signal(self.view.login_button, 'click', lambda _: self.handle_login())

    def handle_login(self):
        self.view.notifier.clear_msg()
        user = self.view.username_editor.get_edit_text()
        password = self.view.password_editor.get_edit_text()

        if not user or not password:
            self.view.notifier.error_msg('Enter your username and password')
            return

        try:
            logged_in = self.client.login(user, password)
        except Exception as e:
            self.view.notifier.error_msg(e.args[0])
            return

        if logged_in:
            self.view.notifier.info_msg('Login succesful!')
            self.loop.projects_view()
        else:
            self.view.notifier.error_msg(self.client.last_error['detail'])


class ProjectsController(Controller):
    def __init__(self, loop, view):
        self.loop = loop
        self.view = view
