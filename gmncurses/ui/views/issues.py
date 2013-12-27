# -*- coding: utf-8 -*-

"""
gmncurses.ui.views.issues
~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import urwid

from gmncurses.ui import widgets

from . import base


class ProjectIssuesSubView(base.SubView):
    help_info = (
       ( "Issues Movements:", (
           ("↑ | k | ctrl p", "Move Up"),
           ("↓ | j | ctrl n", "Move Down"),
           #("← | h | ctrl b", "Move Left"),
           #("→ | l | ctrl f", "Move Right"),
       )),
       ( "Issue Actions:", (
           ("i", "Create new Issue (TODO)"),
           ("e", "Edit selected Issue (TODO)"),
           ("Supr", "Delete selected Issue (TODO)"),
       )),
    )

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

    def open_help_popup(self):
        self.help_popup = widgets.HelpPopup("Issues Help Info", self.help_info)
        # FIXME: Calculate the popup size
        self.parent.show_widget_on_top(self.help_popup, 60, 17)

    def close_help_popup(self):
        self.parent.hide_widget_on_top()
