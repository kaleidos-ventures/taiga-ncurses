# -*- coding: utf-8 -*-

"""
gmncurses.ui.views.milestones
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import urwid

from gmncurses.ui.widgets import generic, milestones

from . import base


class ProjectMilestoneSubView(base.SubView):
    help_info = (
       ( "Milestone Movements:", (
           ("↑ | k | ctrl p", "Move Up"),
           ("↓ | j | ctrl n", "Move Down"),
           #("← | h | ctrl b", "Move Left"),
           #("→ | l | ctrl f", "Move Right"),
       )),
       ( "Task Actions:", (
           ("m", "Change to another Milestone"),
           ("i", "Create new Task (TODO)"),
           ("e", "Edit selected Task/Us (TODO)"),
           ("Supr", "Delete selected Task (TODO)"),
       )),
    )

    def __init__(self, parent_view, project, notifier, tabs):
        super().__init__(parent_view)

        self.project = project
        self.notifier = notifier

        self.info = milestones.MilestoneInfo(project)
        self.stats = milestones.MilestoneStats(project)
        self.taskboard = milestones.MilestoneTaskboard(project)

        self.widget = urwid.ListBox(urwid.SimpleListWalker([
            tabs,
            generic.box_solid_fill(" ", 1),
            self.info,
            generic.box_solid_fill(" ", 1),
            self.stats,
            generic.box_solid_fill(" ", 1),
            self.taskboard,
        ]))

    def open_milestones_selector_popup(self, current_milestone={}):
        self.milestone_selector_popup = milestones.MIlestoneSelectorPopup(self.project, current_milestone)
        # FIXME: Calculate the popup size
        self.parent.show_widget_on_top(self.milestone_selector_popup, 100, 28)

    def close_milestone_selector_popup(self):
        del self.milestone_selector_popup
        self.parent.hide_widget_on_top()

    def open_help_popup(self):
        self.help_popup = generic.HelpPopup("Milestone Help Info", self.help_info)
        # FIXME: Calculate the popup size
        self.parent.show_widget_on_top(self.help_popup, 60, 17)

    def close_help_popup(self):
        del self.help_popup
        self.parent.hide_widget_on_top()
