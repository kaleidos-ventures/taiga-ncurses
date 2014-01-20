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
           ("n", "Create new Issue"),
           ("e", "Edit selected Issue"),
           ("Supr", "Delete selected Issue"),
           ("f", "Filter issues"),
       )),
    )

    def __init__(self, parent_view, project, notifier, tabs):
        super().__init__(parent_view)

        self.project = project
        self.notifier = notifier
        self.filters = {}

        self.stats = issues.IssuesStats(project)
        self.filters_info = issues.IssuesFiltersInfo(project, self.filters)
        self.issues = issues.IssuesList(project)

        list_walker = urwid.SimpleFocusListWalker([
            tabs,
            generic.box_solid_fill(" ", 1),
            self.stats,
            generic.box_solid_fill(" ", 1),
            self.filters_info,
            self.issues
        ])
        list_walker.set_focus(5)
        self.widget = urwid.ListBox(list_walker)

    def set_filters(self, filters):
        self.filters = filters
        self.filters_info.set_filters(self.filters)

    def open_issue_form(self, issue={}):
        self.issue_form = issues.IssueForm(self.project, issue=issue)
        # FIXME: Calculate the form size
        self.parent.show_widget_on_top(self.issue_form, 80, 23)

    def close_issue_form(self):
        del self.issue_form
        self.parent.hide_widget_on_top()

    def get_issue_form_data(self):
        if hasattr(self, "issue_form"):
            data = {
                "subject": self.issue_form.subject,
                "type": self.issue_form.type,
                "status": self.issue_form.status,
                "priority": self.issue_form.priority,
                "severity": self.issue_form.severity,
                "assigned_to": self.issue_form.assigned_to,
                "tags": self.issue_form.tags,
                "description": self.issue_form.description,
                "project": self.project["id"],
            }
            return data
        return {}

    def open_filters_popup(self):
        self.filters_popup = issues.FiltersPopup(self.project, self.filters)
        # FIXME: Calculate the popup size
        self.parent.show_widget_on_top(self.filters_popup, 130, 28)

    def close_filters_popup(self):
        del self.filters_popup
        self.parent.hide_widget_on_top()

    def get_filters_popup_data(self):
        if hasattr(self, "filters_popup"):
            return self.filters_popup.filters
        return {}
