# -*- coding: utf-8 -*-

"""
gmncurses.ui.views.backlog
~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import urwid

from gmncurses.ui import widgets

from . import base


class ProjectBacklogSubView(base.SubView):
    def __init__(self, parent_view, project, notifier, tabs):
        super().__init__(parent_view)

        self.project = project
        self.notifier = notifier

        self.stats = widgets.ProjectBacklogStats(project)
        self.user_stories = widgets.UserStoryList(project)

        list_walker = urwid.SimpleFocusListWalker([
            tabs,
            widgets.box_solid_fill(" ", 1),
            self.stats,
            widgets.box_solid_fill(" ", 1),
            self.user_stories
        ])
        list_walker.set_focus(4)
        self.widget = urwid.ListBox(list_walker)

    def open_user_story_form(self, user_story={}):
        self.user_story_form = widgets.UserStoryForm(self.project, user_story=user_story)
        # FIXME: Calculate the form size
        self.parent.show_widget_on_top(self.user_story_form, 150, 22)

    def close_user_story_form(self):
        self.parent.hide_widget_on_top()

    def get_user_story_form_data(self):
        data = {
            "subject": self.user_story_form.subject,
            "points": self.user_story_form.points,
            "status": self.user_story_form.status,
            "tags": self.user_story_form.tags,
            "description": self.user_story_form.description,
            "team_requirement": self.user_story_form.team_requirement,
            "client_requirement": self.user_story_form.client_requirement,
            "project": self.project["id"],
        }
        return data

