# -*- coding: utf-8 -*-

"""
ui.widgets
~~~~~~~~~
"""

import urwid

from .mixins import FormMixin, NotifierMixin

PALETTE = [
    ('green', 'dark green', 'default'),
    ('editor', 'white', 'black'),
    ('password-editor', 'light red', 'black'),
    ('save-button', 'dark magenta', 'default'),
    ('error', 'white', 'dark red'),
    ('info', 'white', 'dark blue'),
]


def wrap_in_whitespace(widget, cls=urwid.Columns):
    whitespace = urwid.SolidFill(' ')
    return cls([whitespace, widget, whitespace])


def center(widget):
    return wrap_in_whitespace(wrap_in_whitespace(widget), cls=urwid.Pile)


def banner():
    bt = urwid.BigText('GreenMine', font=urwid.font.HalfBlock7x7Font())
    btwp = urwid.Padding(bt, 'center', width='clip')
    return urwid.AttrWrap(btwp, 'green')


def username_prompt(username_text, editor, max_prompt_padding):
    username = urwid.Text(username_text, 'center')
    return urwid.Columns([(len(username_text), username),
                          (max_prompt_padding - len(username_text), urwid.Text('')),
                          urwid.AttrWrap(editor, 'editor')])


def password_prompt(password_text, editor, max_prompt_padding):
    password = urwid.Text(password_text, 'center')
    return urwid.Columns([(len(password_text), password),
                          (max_prompt_padding - len(password_text), urwid.Text('')),
                          urwid.AttrWrap(editor, 'password-editor')])


def wrap_save_button(button):
    return urwid.AttrWrap(urwid.LineBox(button), 'save-button')


def button(text, align=None):
    return urwid.Button(('center' if align is None else align, text))


def editor(mask=None):
    if mask is None:
        return urwid.Edit()
    else:
        return urwid.Edit(mask=mask)


class Login(FormMixin, urwid.ListBox):
    def __init__(self, widgets):
        super(Login, self).__init__(urwid.SimpleListWalker(widgets))


class Notifier(NotifierMixin, urwid.Text):
    pass
