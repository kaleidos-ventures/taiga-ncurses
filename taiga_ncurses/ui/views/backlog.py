# -*- coding: utf-8 -*-

"""
taiga_ncurses.ui.views.backlog
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import urwid

from taiga_ncurses.ui.widgets import generic, backlog

from . import base


class ProjectBacklogSubView(base.SubView):
    help_popup_title = "Backlog Help Info"
    help_popup_info = base.SubView.help_popup_info + (
       ( "Backlog Movements:", (
           ("↑ | k | ctrl p", "Move Up"),
           ("↓ | j | ctrl n", "Move Down"),
           ("← | h | ctrl b", "Move Left"),
           ("→ | l | ctrl f", "Move Right"),
       )),
       ( "User Stories Actions:", (
           ("n", "Create new US"),
           ("N", "Create new USs in bulk"),
           ("e", "Edit selected US"),
           ("Supr", "Delete selected US"),
           ("K", "Move selected US up"),
           ("J", "Move selected US down"),
           ("w", "Save the position of all USs"),
           ("m", "Move selected US to a Milestone"),
           ("r", "Refresh the screen")
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
        self.parent.show_widget_on_top(self.user_story_form, 80, 24)

    def close_user_story_form(self):
        del self.user_story_form
        self.parent.hide_widget_on_top()

    def get_user_story_form_data(self):
        data = {}
        if hasattr(self, "user_story_form"):
            data.update({
                "subject": self.user_story_form.subject,
                "milestone": self.user_story_form.milestone,
                "points": self.user_story_form.points,
                "status": self.user_story_form.status,
                "is_blocked": self.user_story_form.is_blocked,
                "blocked_note": self.user_story_form.blocked_note,
                "tags": self.user_story_form.tags,
                "description": self.user_story_form.description,
                "team_requirement": self.user_story_form.team_requirement,
                "client_requirement": self.user_story_form.client_requirement,
                "project": self.project["id"],
            })
        return data

    def open_user_stories_in_bulk_form(self):
        self.user_stories_in_bulk_form = backlog.UserStoriesInBulkForm(self.project)
        # FIXME: Calculate the form size
        self.parent.show_widget_on_top(self.user_stories_in_bulk_form, 80, 24)

    def close_user_stories_in_bulk_form(self):
        del self.user_stories_in_bulk_form
        self.parent.hide_widget_on_top()

    def get_user_stories_in_bulk_form_data(self):
        data = {}
        if hasattr(self, "user_stories_in_bulk_form"):
            data.update({
                "bulkStories": self.user_stories_in_bulk_form.subjects,
                "projectId": self.project["id"],
            })
        return data

    def open_milestones_selector_popup(self, user_story={}):
        self.milestone_selector_popup = backlog.MIlestoneSelectorPopup(self.project, user_story)
        # FIXME: Calculate the popup size
        self.parent.show_widget_on_top(self.milestone_selector_popup, 100, 30)

    def close_milestone_selector_popup(self):
        del self.milestone_selector_popup
        self.parent.hide_widget_on_top()
