# -*- coding: utf-8 -*-

import functools

import urwid

from gmncurses.api.client import GreenMineClient
from gmncurses.ui import widgets


# TODO: config
GREENMINE_HOST = 'http://api.greenmine.kaleidos.net'


def debug(loop):
    loop.screen.stop()
    import ipdb; ipdb.set_trace()
    loop.screen.start()


def key_handler(loop, key):
    if key == 'q':
        raise urwid.ExitMainLoop
    elif key == 'D':
        debug(loop)
    return key


def main():
    # UI
    header = widgets.banner()

    # :: Login form
    username_text = 'user'
    password_text = 'password'
    max_prompt_length = max(len(username_text), len(password_text))
    max_prompt_padding = max_prompt_length + 2

    username_editor = widgets.editor()
    username_prompt = widgets.username_prompt(username_text, username_editor, max_prompt_padding)
    password_editor = widgets.editor(mask='♥')
    password_prompt = widgets.password_prompt(password_text, password_editor, max_prompt_padding)

    save_button = widgets.button('Save')
    save_button_widget = widgets.wrap_save_button(save_button)

    notifier = widgets.Notifier("")
    login_widget = widgets.Login([header, username_prompt, password_prompt, save_button_widget, notifier])

    ui = widgets.center(login_widget)

    # Main loop
    loop = urwid.MainLoop(ui, palette=widgets.PALETTE, handle_mouse=True)
    loop.unhandled_input = functools.partial(key_handler, loop)

    # API
    gm = GreenMineClient(GREENMINE_HOST)

    # Signal handlers
    def handle_login():
        user, password = username_editor.get_edit_text(), password_editor.get_edit_text()
        if not user or not password:
            notifier.error_msg('Enter your username and password')
            return

        # FIXME: Login with the API client
        try:
            logged_in = gm.login(user, password)
        except Exception as e:
            notifier.error_msg(e.args[0])
            return

        if logged_in:
            notifier.info_msg('Login succesful!')
        else:
            notifier.error_msg(gm.last_error['detail'])


    urwid.connect_signal(save_button, 'click', lambda _: handle_login())

    loop.run()
