# -*- coding: utf-8 -*-

"""
gmncurses.ui.views.issues
~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import urwid

from gmncurses.ui import widgets

from . import base


class ProjectIssuesSubView(base.SubView):
    def __init__(self, parent_view, project, notifier, tabs):
        super().__init__(parent_view)

        self.project = project
        self.notifier = notifier

        self.stats = widgets.ProjectIssuesStats(project)
        self.issues = widgets.IssuesList(project)

        list_walker = urwid.SimpleFocusListWalker([
            tabs,
            widgets.box_solid_fill(" ", 1),
            self.stats,
            widgets.box_solid_fill(" ", 1),
            self.issues
        ])
        list_walker.set_focus(4)
        self.widget = urwid.ListBox(list_walker)
