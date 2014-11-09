# -*- coding: utf-8 -*-

"""
taiga_ncurses.ui.signals
~~~~~~~~~~~~~~~~~~~~~~~~
"""

import urwid

connect = urwid.connect_signal
disconnect = urwid.disconnect_signal

def emit(widget, signal):
    widget._emit(signal)
