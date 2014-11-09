# -*- coding: utf-8 -*-

"""
taiga_ncurses.ui.widgets.mixins
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import urwid


class IgnoreKeyPressMixin:
    def keypress(self, size, key):
        return key


class KeyPressMixin:
    signals = ["click"]

    def keypress(self, size, key):
        """
        Send 'click' signal on 'activate' command.

        >>> assert Button._command_map[' '] == 'activate'
        >>> assert Button._command_map['enter'] == 'activate'
        >>> size = (15,)
        >>> b = Button("Cancel")
        >>> clicked_buttons = []
        >>> def handle_click(button):
        ...     clicked_buttons.append(button.label)
        >>> connect_signal(b, 'click', handle_click)
        >>> b.keypress(size, 'enter')
        >>> b.keypress(size, ' ')
        >>> clicked_buttons # ... = u in Python 2
        [...'Cancel', ...'Cancel']
        """
        if self._command_map[key] != urwid.ACTIVATE:
            return key

        self._emit('click')

    def mouse_event(self, size, event, button, x, y, focus):
        """
        Send 'click' signal on button 1 press.

        >>> size = (15,)
        >>> b = Button("Ok")
        >>> clicked_buttons = []
        >>> def handle_click(button):
        ...     clicked_buttons.append(button.label)
        >>> connect_signal(b, 'click', handle_click)
        >>> b.mouse_event(size, 'mouse press', 1, 4, 0, True)
        True
        >>> b.mouse_event(size, 'mouse press', 2, 4, 0, True) # ignored
        False
        >>> clicked_buttons # ... = u in Python 2
        [...'Ok']
        """
        if button != 1 or not urwid.util.is_mouse_press(event):
            return False

        self._emit('click')
        return True


class FormMixin:
    FORM_KEYS = {
        "tab": "down",
        "shift tab": "up",
    }

    def keypress(self, size, key):
        key = self.FORM_KEYS.get(key, key)
        return super().keypress(size, key)

class ViMotionMixin:
    VI_KEYS = {
        "j": "down",
        "k": "up",
        "h": "left",
        "l": "right",
    }

    def keypress(self, size, key):
        key = self.VI_KEYS.get(key, key)
        return super().keypress(size, key)

class EmacsMotionMixin:
    EMACS_KEYS = {
        "ctrl n": "down",
        "ctrl p": "up",
        "ctrl b": "left",
        "ctrl f": "right",
    }

    def keypress(self, size, key):
        key = self.EMACS_KEYS.get(key, key)
        return super().keypress(size, key)

class NotifierMixin:
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


class PlainButtonMixin:
    button_left = urwid.Text("")
    button_right = urwid.Text("")


class NonSelectableMixin:
    def selectable(self):
        return False
