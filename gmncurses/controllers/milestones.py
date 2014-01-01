# -*- coding: utf-8 -*-

"""
gmncurses.controllers.milestone
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from concurrent.futures import wait
import functools

from gmncurses.config import ProjectMilestoneKeys
from gmncurses.ui import signals
import gmncurses.data


from . import base


class ProjectMilestoneSubController(base.Controller):
    def __init__(self, view, executor, state_machine):
        self.view = view
        self.executor = executor
        self.state_machine = state_machine

    def handle(self, key):
        if key == ProjectMilestoneKeys.RELOAD:
            self.load()
        elif key == ProjectMilestoneKeys.HELP:
            self.help_info()
        else:
            super().handle(key)

    def load(self):
        self.state_machine.transition(self.state_machine.PROJECT_MILESTONES)

        self.view.notifier.info_msg("Fetching Stats and User stories")

        last_milestone_id = gmncurses.data.current_sprint_id(self.view.project)

        milestone_f = self.executor.milestone(last_milestone_id, self.view.project)
        milestone_f.add_done_callback(self.handle_milestone)

        milestone_stats_f = self.executor.milestone_stats(last_milestone_id, self.view.project)
        milestone_stats_f.add_done_callback(self.handle_milestone_stats)

        user_stories_f = self.executor.user_stories(last_milestone_id, self.view.project)
        user_stories_f.add_done_callback(self.handle_user_stories)

        milestone_tasks_f = self.executor.milestone_tasks(last_milestone_id, self.view.project)
        milestone_tasks_f.add_done_callback(self.handle_milestone_tasks)

        futures = (milestone_tasks_f, user_stories_f)
        futures_completed_f = self.executor.pool.submit(lambda : wait(futures, 10))
        futures_completed_f.add_done_callback(self.handle_user_stories_and_task_info_fetched)

    def help_info(self):
        self.view.open_help_popup()

        signals.connect(self.view.help_popup.close_button, "click",
                lambda _: self.close_help_info())

    def close_help_info(self):
        self.view.close_help_popup()

    def handle_milestone(self, future):
        self.milestone = future.result()
        if self.milestone:
            self.view.info.populate(self.milestone)
            self.state_machine.refresh()

    def handle_milestone_stats(self, future):
        self.milestone_stats = future.result()
        if self.milestone_stats:
            self.view.stats.populate(self.milestone_stats)
            self.state_machine.refresh()

    def handle_user_stories(self, future):
        self.user_stories = future.result()

    def handle_milestone_tasks(self, future):
        self.milestone_tasks = future.result()

    def handle_user_stories_and_task_info_fetched(self, future_with_results):
        done, not_done = future_with_results.result()
        if len(done) == 2:
            self.view.taskboard.populate(self.user_stories, self.milestone_tasks)
            self.view.notifier.info_msg("User stories and tasks fetched")
            self.state_machine.refresh()
        else:
            # TODO retry failed operations
            self.view.notifier.error_msg("Failed to fetch milestone data (user stories or task)")
