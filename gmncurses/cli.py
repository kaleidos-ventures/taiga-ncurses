# -*- coding: utf-8 -*-

import functools

import urwid

from gmncurses.api.client import GreenMine


# TODO: config
GREENMINE_HOST = 'http://api.greenmine.kaleidos.net'

PALETTE = [
    ('green', 'dark green', 'default'),
    ('editor', 'white', 'black'),
    ('password-editor', 'light red', 'black'),
    ('save-button', 'dark magenta', 'default'),
    ('error', 'white', 'dark red'),
    ('info', 'white', 'dark blue'),
]

class FormMixin(object):
    KEYS = { 'tab': 'down', 'shift tab': 'up', }

    def keypress(self, size, key):
        key = self.KEYS.get(key, key)
        return super(FormMixin, self).keypress(size, key)


class Login(FormMixin, urwid.ListBox):
    def __init__(self, widgets):
        super(Login, self).__init__(urwid.SimpleListWalker(widgets))


class NotifierMixin(object):
    def error_msg(self, text):
        self.set_text(('error', text))

    def info_msg(self, text):
        self.set_text(('info', text))

    def clear_msg(self):
        self.set_text('')


class Notifier(NotifierMixin, urwid.Text):
    pass


def wrap_in_whitespace(widget, cls=urwid.Columns):
    whitespace = urwid.SolidFill(' ')
    return cls([whitespace, widget, whitespace])

def banner_widget():
    bt = urwid.BigText('GreenMine', font=urwid.font.HalfBlock7x7Font())
    btwp = urwid.Padding(bt, 'center', width='clip')
    return urwid.AttrWrap(btwp, 'green')

def username_prompt_widget(username_text, editor, max_prompt_padding):
    username = urwid.Text(username_text, 'center')
    return urwid.Columns([(len(username_text), username),
                          (max_prompt_padding - len(username_text), urwid.Text('')),
                          urwid.AttrWrap(editor, 'editor')])

def password_prompt_widget(password_text, editor, max_prompt_padding):
    password = urwid.Text(password_text, 'center')
    return urwid.Columns([(len(password_text), password),
                          (max_prompt_padding - len(password_text), urwid.Text('')),
                          urwid.AttrWrap(editor, 'password-editor')])

def wrap_save_button_widget(button):
    return urwid.AttrWrap(urwid.LineBox(button), 'save-button')


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
    header = banner_widget()

    # :: Login form
    username_text = 'user'
    password_text = 'password'
    max_prompt_length = max(len(username_text), len(password_text))
    max_prompt_padding = max_prompt_length + 2

    username_editor = urwid.Edit()
    username_prompt = username_prompt_widget(username_text, username_editor, max_prompt_padding)
    password_editor = urwid.Edit(mask='♥')
    password_prompt = password_prompt_widget(password_text, password_editor, max_prompt_padding)

    save_button = urwid.Button(('center', 'Save'))
    save_button_widget = wrap_save_button_widget(save_button)

    notifier = Notifier("")
    login_widget = Login([header, username_prompt, password_prompt, save_button_widget, notifier])

    ui = wrap_in_whitespace(wrap_in_whitespace(login_widget), cls=urwid.Pile)

    # Main loop
    loop = urwid.MainLoop(ui, palette=PALETTE, handle_mouse=True)
    loop.unhandled_input = functools.partial(key_handler, loop)

    # API
    gm = GreenMine(GREENMINE_HOST)

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
