# -*- coding: utf-8 -*-

"""
taiga_ncurses.ui.views.milestones
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import urwid

from taiga_ncurses.ui.widgets import generic, milestones, backlog

from . import base


class ProjectMilestoneSubView(base.SubView):
    help_popup_title = "Milestone Help Info"
    help_popup_info = base.SubView.help_popup_info + (
       ( "Milestone Movements:", (
           ("↑ | k | ctrl p", "Move Up"),
           ("↓ | j | ctrl n", "Move Down"),
           ("← | h | ctrl b", "Move Left"),
           ("→ | l | ctrl f", "Move Right"),
       )),
       ( "Milestone Actions:", (
           ("m", "Change to another Milestone"),
           ("N", "Create new US"),
           ("n", "Create new Task"),
           ("e", "Edit selected US/Task"),
           ("Supr", "Delete selected US/Task"),
           ("r", "Refresh the screen")
       )),
    )

    def __init__(self, parent_view, project, notifier, tabs):
        super().__init__(parent_view)
        self.notifier = notifier

        self._project = project
        self._milestone = {}
        self._user_stories = []
        self._tasks = []

        self.info = milestones.MilestoneInfo(self._project)
        self.stats = milestones.MilestoneStats(self._project)
        self.taskboard = milestones.MilestoneTaskboard(self._project)

        self.widget = urwid.ListBox(urwid.SimpleListWalker([
            tabs,
            generic.box_solid_fill(" ", 1),
            self.info,
            generic.box_solid_fill(" ", 1),
            self.stats,
            generic.box_solid_fill(" ", 1),
            # TODO: FIXME: Calculate the row size wehn populate the tb.
            urwid.BoxAdapter(self.taskboard, 46),
        ]))

    def open_user_story_form(self, user_story={}):
        self.user_story_form = backlog.UserStoryForm(self._project, user_story=user_story)
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
                "project": self._project["id"]
            })
        return data

    def open_task_form(self, task={}):
        self.task_form = milestones.TaskForm(self._project, self._user_stories, task=task)
        # FIXME: Calculate the form size
        self.parent.show_widget_on_top(self.task_form, 80, 21)

    def close_task_form(self):
        del self.task_form
        self.parent.hide_widget_on_top()

    def get_task_form_data(self):
        data = {}
        if hasattr(self, "task_form"):
            data.update({
                "subject": self.task_form.subject,
                "user_story": self.task_form.user_story,
                "status": self.task_form.status,
                "assigned_to": self.task_form.assigned_to,
                "is_iocaine": self.task_form.is_iocaine,
                "tags": self.task_form.tags,
                "description": self.task_form.description,
                "project": self._project["id"],
                "milestone": self._milestone["id"]
            })
        return data

    def open_milestones_selector_popup(self, current_milestone={}):
        self.milestone_selector_popup = milestones.MIlestoneSelectorPopup(self._project, current_milestone)
        # FIXME: Calculate the popup size
        self.parent.show_widget_on_top(self.milestone_selector_popup, 100, 28)

    def close_milestone_selector_popup(self):
        del self.milestone_selector_popup
        self.parent.hide_widget_on_top()
