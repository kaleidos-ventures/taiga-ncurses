# -*- coding: utf-8 -*-

"""
taiga_ncurses.ui.views.auth
~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from taiga_ncurses.ui.widgets import generic, auth

from . import base


class LoginView(base.View):
    login_button = None

    def __init__(self, username_text, password_text):
        # Header
        header = generic.banner()
        # Username and password prompts
        max_prompt_length = max(len(username_text), len(password_text))
        max_prompt_padding = max_prompt_length + 2

        self._username_editor = generic.editor()
        username_prompt = auth.username_prompt(username_text, self._username_editor, max_prompt_padding)
        self._password_editor = generic.editor(mask="♥")
        password_prompt = auth.password_prompt(password_text, self._password_editor, max_prompt_padding)
        # Login button
        self.login_button = generic.button("login")
        login_button_widget = auth.wrap_login_button(self.login_button)
        # Notifier
        self.notifier = generic.Notifier("")

        login_widget = auth.Login([header,
                                      generic.box_solid_fill(" ", 2),
                                      username_prompt,
                                      generic.box_solid_fill(" ", 1),
                                      password_prompt,
                                      generic.box_solid_fill(" ", 2),
                                      login_button_widget,
                                      generic.box_solid_fill(" ", 1),
                                      self.notifier])
        self.widget = generic.center(login_widget)

    @property
    def username(self):
        return self._username_editor.get_edit_text()

    @property
    def password(self):
        return self._password_editor.get_edit_text()
