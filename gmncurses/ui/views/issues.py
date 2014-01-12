# -*- coding: utf-8 -*-

"""
gmncurses.ui.views.issues
~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import urwid

from gmncurses.ui.widgets import generic, issues

from . import base


class ProjectIssuesSubView(base.SubView):
    help_popup_title = "Issues Help Info"
    help_popup_info = base.SubView.help_popup_info + (
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
        self.filters = {}

        self.stats = issues.IssuesStats(project)
        self.issues = issues.IssuesList(project)

        list_walker = urwid.SimpleFocusListWalker([
            tabs,
            generic.box_solid_fill(" ", 1),
            self.stats,
            generic.box_solid_fill(" ", 1),
            self.issues
        ])
        list_walker.set_focus(4)
        self.widget = urwid.ListBox(list_walker)

    def open_filters_popup(self):
        self.filters_popup = issues.FiltersPopup(self.project)
        # FIXME: Calculate the popup size
        self.parent.show_widget_on_top(self.filters_popup, 130, 28)

    def close_filters_popup(self):
        del self.filters_popup
        self.parent.hide_widget_on_top()

    def get_filters_popup_data(self):
        if hasattr(self, "filters_popup"):
            return self.filters_popup.filters
        return {}
