# -*- coding: utf-8 -*-

"""
ui.mixins
~~~~~~~~~
"""


class FormMixin(object):
    KEYS = { 'tab': 'down', 'shift tab': 'up', }

    def keypress(self, size, key):
        key = self.KEYS.get(key, key)
        return super(FormMixin, self).keypress(size, key)


class NotifierMixin(object):
    ALIGN = 'center'

    def error_msg(self, text):
        self.set_text(('error', text))
        self.set_align_mode(self.ALIGN)

    def info_msg(self, text):
        self.set_text(('info', text))
        self.set_align_mode(self.ALIGN)

    def clear_msg(self):
        self.set_text('')

