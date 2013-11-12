# -*- coding: utf-8 -*-

import functools

import urwid

from gmncurses.api.client import GreenMine


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

class UI(FormMixin, urwid.ListBox):
    def __init__(self, widgets):
        self._msg = urwid.Text('')
        widgets.append(self._msg)
        super(UI, self).__init__(urwid.SimpleListWalker(widgets))

    def error_msg(self, text):
        self._msg.set_text(('error', text))

    def info_msg(self, text):
        self._msg.set_text(('info', text))

    def clear_msg(self):
        self._msg.set_text('')


def debug(loop):
    loop.screen.stop()
    import ipdb; ipdb.set_trace()
    loop.screen.start()

def key_handler(loop, key):
    if key == 'q':
        raise urwid.ExitMainLoop
    elif key == 'D':
        debug(loop)
    else:
        debug(loop)
    return key


bt = urwid.BigText('Greenmine', font=urwid.font.HalfBlock7x7Font())
bt = urwid.Padding(bt, 'center', width='clip')
header = urwid.AttrWrap(bt, 'green')

username_text = 'user'
password_text = 'password'

max_prompt_length = max(len(username_text), len(password_text))
max_prompt_padding = max_prompt_length + 2

username = urwid.Text(username_text, 'center')
password = urwid.Text(password_text, 'center')

username_editor = urwid.Edit()
username_prompt = urwid.Columns([(len(username_text), username),
                                 (max_prompt_padding - len(username_text), urwid.Text('')),
                                  urwid.AttrWrap(username_editor, 'editor')])

password_editor = urwid.Edit(mask='♥')
password_prompt = urwid.Columns([(len(password_text), password),
                                 (max_prompt_padding - len(password_text), urwid.Text('')),
                                  urwid.AttrWrap(password_editor, 'password-editor')])


def handle_login(gm, loop, save_btn):
    user, password = username_editor.get_edit_text(), password_editor.get_edit_text()
    if not user or not password:
        loop.widget.focus.error_msg('Enter your username and password')
        loop.set_alarm_in(4, lambda *args: loop.widget.focus.clear_msg())
        return

    # FIXME: Login with the API client
    try:
        logged_in = gm.login(user, password)
    except Exception as e:
        return loop.widget.focus.error_msg(e.args[0])

    if logged_in:
        loop.widget.focus.info_msg('Login succesful!')
    else:
        loop.widget.focus.error_msg(gm.last_error['detail'])


save_button = urwid.Button(('center', 'Save'))
save_button_widget = urwid.AttrWrap(urwid.LineBox(save_button), 'save-button')

whitespace = urwid.SolidFill(' ')
ui = UI([ header, username_prompt, password_prompt, save_button_widget,])
ui = urwid.Columns([whitespace, ui, whitespace])

GREENMINE_HOST = 'http://greenmine.kaleidos.net'
gm = GreenMine(GREENMINE_HOST)
loop = urwid.MainLoop(ui, palette=PALETTE, handle_mouse=True)
loop.unhandled_input = functools.partial(key_handler, loop)
urwid.connect_signal(save_button, 'click', functools.partial(handle_login, gm, loop))
loop.run()
