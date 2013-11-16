# -*- coding: utf-8 -*-

"""
gmncurses.core
~~~~~~~~~~~~~~
"""

import functools

import urwid

from gmncurses.ui import widgets
from gmncurses.config import Keys


def debug(loop):
    loop.screen.stop()
    import ipdb; ipdb.set_trace()
    loop.screen.start()


def key_handler(loop, key):
    if key == Keys.QUIT:
        raise urwid.ExitMainLoop
    elif key == Keys.DEBUG:
        debug(loop)
    return key


class GreenMineCore(object):
    def __init__(self, client):
        self.client = client

        # UI
        header = widgets.banner()

        # - Login form
        username_text = 'user'
        password_text = 'password'
        max_prompt_length = max(len(username_text), len(password_text))
        max_prompt_padding = max_prompt_length + 2

        self.username_editor = widgets.editor()
        username_prompt = widgets.username_prompt(username_text, self.username_editor, max_prompt_padding)
        self.password_editor = widgets.editor(mask='♥')
        password_prompt = widgets.password_prompt(password_text, self.password_editor, max_prompt_padding)

        save_button = widgets.button('Save')
        save_button_widget = widgets.wrap_save_button(save_button)

        self.notifier = widgets.Notifier("")
        login_widget = widgets.Login([header, username_prompt, password_prompt, save_button_widget, self.notifier])

        ui = widgets.center(login_widget)

        # Main Loop
        self.loop = urwid.MainLoop(ui, palette=widgets.PALETTE, handle_mouse=True)
        self.loop.unhandled_input = functools.partial(key_handler, self.loop)

        # Signal handlers
        urwid.connect_signal(save_button, 'click', lambda _: self.handle_login())

    def run(self):
        self.loop.run()

    def handle_login(self):
        user, password = self.username_editor.get_edit_text(), self.password_editor.get_edit_text()
        if not user or not password:
            self.notifier.error_msg('Enter your username and password')
            return

        try:
            logged_in = self.client.login(user, password)
        except Exception as e:
            self.notifier.error_msg(e.args[0])
            return

        if logged_in:
            self.notifier.info_msg('Login succesful!')
            projects = self.client.get_projects()
            debug(self.loop)
        else:
            self.notifier.error_msg(self.client.last_error['detail'])
