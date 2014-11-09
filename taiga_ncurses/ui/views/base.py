# -*- coding: utf-8 -*-

"""
taiga_ncurses.ui.views.base
~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import urwid

from taiga_ncurses.ui.widgets import generic


class View:
    widget = None
    notifier = None

    def show_widget_on_top(self, top_widget, width, height, align='center', valign='middle',
                           min_height=10, min_width=10):
        self.widget.set_body(self._build_overlay_widget(top_widget, align, width, valign, height,
                                                        min_width, min_height))

    def hide_widget_on_top(self):
        self.widget.set_body(self.widget.get_body().bottom_w)

    def _build_overlay_widget(self, top_widget, align, width, valign, height, min_width, min_height):
        return urwid.Overlay(top_w=urwid.Filler(top_widget), bottom_w=self.widget.get_body(),
                       align=align, width=width, valign=valign, height=height,
                       min_width=min_width, min_height=min_height)


class SubView:
    parent = None
    widget = None
    help_popup_title = "Help Info"
    help_popup_info = (
       ( "General", (
           ("B", "Go to Backlog Panel"),
           ("M", "Go to Milestones Panel"),
           ("I", "Go to Issues Panel"),
           ("W", "Go to Wiki Panel"),
           ("A", "Go to Admin Panel"),
           ("P", "Go back to the Projects Panel"),
       )),
    )
    def __init__(self, parent_view=None):
        self.parent = parent_view

    def open_help_popup(self):
        self.help_popup = generic.HelpPopup(self.help_popup_title, self.help_popup_info)
        row = 5 + sum([3 + len(s[1]) for s in self.help_popup_info])
        col = 60

        self.parent.show_widget_on_top(self.help_popup, col, row)

    def close_help_popup(self):
        del self.help_popup
        self.parent.hide_widget_on_top()
