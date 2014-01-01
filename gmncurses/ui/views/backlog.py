# -*- coding: utf-8 -*-

"""
gmncurses.ui.views.backlog
~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import urwid

from gmncurses.ui.widgets import generic, backlog

from . import base


class ProjectBacklogSubView(base.SubView):
    help_info = (
       ( "Backlog Movements:", (
           ("↑ | k | ctrl p", "Move Up"),
           ("↓ | j | ctrl n", "Move Down"),
           #("← | h | ctrl b", "Move Left"),
           #("→ | l | ctrl f", "Move Right"),
       )),
       ( "User Stories Actions:", (
           ("i", "Create new US"),
           ("e", "Edit selected US"),
           ("Supr", "Delete selected US"),
           ("K", "Move selected US up"),
           ("J", "Move selected US down"),
           ("w", "Save the position of all USs"),
       )),
    )

    def __init__(self, parent_view, project, notifier, tabs):
        super().__init__(parent_view)

        self.project = project
        self.notifier = notifier

        self.stats = backlog.BacklogStats(project)
        self.user_stories = backlog.UserStoryList(project)

        list_walker = urwid.SimpleFocusListWalker([
            tabs,
            generic.box_solid_fill(" ", 1),
            self.stats,
            generic.box_solid_fill(" ", 1),
            self.user_stories
        ])
        list_walker.set_focus(4)
        self.widget = urwid.ListBox(list_walker)

    def open_user_story_form(self, user_story={}):
        self.user_story_form = backlog.UserStoryForm(self.project, user_story=user_story)
        # FIXME: Calculate the form size
        self.parent.show_widget_on_top(self.user_story_form, 150, 22)

    def close_user_story_form(self):
        del self.user_story_form
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

    def open_help_popup(self):
        self.help_popup = generic.HelpPopup("Backlog Help Info", self.help_info)
        # FIXME: Calculate the popup size
        self.parent.show_widget_on_top(self.help_popup, 60, 20)

    def close_help_popup(self):
        del self.help_popup
        self.parent.hide_widget_on_top()
