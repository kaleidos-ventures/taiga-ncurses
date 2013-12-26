# -*- coding: utf-8 -*-

"""
gmncurses.ui.views.base
~~~~~~~~~~~~~~~~~~~~~~~
"""

import urwid


class View(object):
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


class SubView(object):
    parent = None
    widget = None

    def __init__(self, parent_view=None):
        self.parent = parent_view
