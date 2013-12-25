# -*- coding: utf-8 -*-

"""
gmncurses.ui.widgets.mixins
~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import urwid


class IgnoreKeyPressMixin(object):
    def keypress(self, size, key):
        return key


class FormMixin(object):
    FORM_KEYS = {
        "tab": "down",
        "shift tab": "up",
    }

    def keypress(self, size, key):
        key = self.FORM_KEYS.get(key, key)
        return super().keypress(size, key)

class ViMotionMixin(object):
    VI_KEYS = {
        "j": "down",
        "k": "up",
        "h": "left",
        "l": "right",
    }

    def keypress(self, size, key):
        key = self.VI_KEYS.get(key, key)
        return super().keypress(size, key)

class EmacsMotionMixin(object):
    EMACS_KEYS = {
        "ctrl n": "down",
        "ctrl p": "up",
        "ctrl b": "left",
        "ctrl f": "right",
    }

    def keypress(self, size, key):
        key = self.EMACS_KEYS.get(key, key)
        return super().keypress(size, key)

class NotifierMixin(object):
    ERROR_PREFIX = ""
    ERROR_ATTR = "error"
    INFO_PREFIX = ""
    INFO_ATTR = "info"
    ALIGN = "center"

    def error_msg(self, text):
        self.set_text((self.ERROR_ATTR, self.ERROR_PREFIX + text))
        self.set_align_mode(self.ALIGN)

    def info_msg(self, text):
        self.set_text((self.INFO_ATTR, self.INFO_PREFIX + text))
        self.set_align_mode(self.ALIGN)

    def clear_msg(self):
        self.set_text("")


class PlainButtonMixin(object):
    button_left = urwid.Text("")
    button_right = urwid.Text("")


class NonSelectableMixin(object):
    def selectable(self):
        return False
