# -*- coding: utf-8 -*-

"""
gmncurses.ui.views.milestones
~~~~~~~~~~~~~~~~~-----------~
"""

import urwid

from gmncurses.ui import widgets

from . import base


class ProjectMilestoneSubView(base.SubView):
    def __init__(self, project, notifier, tabs):
        self.project = project
        self.notifier = notifier

        self.stats = widgets.ProjectSprintsStats(project)
        self.user_stories_list = widgets.ProjectSprintsUserStories(project)

        self.widget = urwid.ListBox(urwid.SimpleListWalker([
            tabs,
            widgets.box_solid_fill(" ", 1),
            self.stats,
            widgets.box_solid_fill(" ", 1),
            self.user_stories_list,
        ]))
