# -*- coding: utf-8 -*-

"""
taiga_ncurses.ui.widgets.projects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import urwid

from . import generic, mixins


class ProjectDetailHeader(mixins.NonSelectableMixin, urwid.WidgetWrap):
    def __init__(self, project):
        text = urwid.Text("TAIGA")
        self.title = urwid.Text(project["name"], align="left")
        self.projects_button = generic.PlainButton("My projects")
        self.account_button = generic.PlainButton("My account")
        cols = urwid.Columns([
            ("weight", 0.1, text),
            ("weight", 0.7, self.title),
            ("weight", 0.1, urwid.AttrMap(self.projects_button, "projects-button")),
            ("weight", 0.1, urwid.AttrMap(self.account_button, "account-button")),
        ])
        super().__init__(urwid.AttrMap(cols, "green-bg"))
