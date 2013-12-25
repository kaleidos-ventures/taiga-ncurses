# -*- coding: utf-8 -*-

"""
gmncurses.controllers.backlog
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from concurrent.futures import wait
import functools

from gmncurses.config import ProjectBacklogKeys
from gmncurses.ui import signals

from . import base


class ProjectBacklogSubController(base.Controller):
    def __init__(self, view, executor, state_machine):
        self.view = view
        self.executor = executor
        self.state_machine = state_machine

    def handle(self, key):
        if key == ProjectBacklogKeys.CREATE_USER_STORY:
            self.new_user_story()
        elif key == ProjectBacklogKeys.EDIT_USER_STORY:
            self.edit_user_story()
        elif key == ProjectBacklogKeys.DELETE_USER_STORY:
            self.delete_user_story()
        elif key == ProjectBacklogKeys.US_UP:
            self.move_current_us_up()
        elif key == ProjectBacklogKeys.US_DOWN:
            self.move_current_us_down()
        elif key == ProjectBacklogKeys.UPDATE_USER_STORIES_ORDER:
            self.update_user_stories_order()
        elif key == ProjectBacklogKeys.RELOAD:
            self.load()
        return super().handle(key)

    def load(self):
        self.state_machine.transition(self.state_machine.PROJECT_BACKLOG)

        self.view.notifier.info_msg("Fetching Stats and User stories")

        project_stats_f = self.executor.project_stats(self.view.project)
        project_stats_f.add_done_callback(self.handle_project_stats)

        user_stories_f = self.executor.unassigned_user_stories(self.view.project)
        user_stories_f.add_done_callback(self.handle_user_stories)

        futures = (project_stats_f, user_stories_f)
        futures_completed_f = self.executor.pool.submit(lambda : wait(futures, 10))
        futures_completed_f.add_done_callback(functools.partial(self.when_backlog_info_fetched,
                                                                info_msg="Project stats and user stories "
                                                                         "fetched",
                                                                error_msg="Failed to fetch project data"))

    def new_user_story(self):
        self.view.open_user_story_form()

        signals.connect(self.view.user_story_form.cancel_button, "click",
                lambda _: self.cancel_user_story_form())
        signals.connect(self.view.user_story_form.save_button, "click",
                lambda _: self.handler_create_user_story_request())

    def edit_user_story(self):
        user_story = self.view.user_stories.widget.get_focus().user_story
        self.view.open_user_story_form(user_story=user_story)

        signals.connect(self.view.user_story_form.cancel_button, "click",
                lambda _: self.cancel_user_story_form())
        signals.connect(self.view.user_story_form.save_button, "click",
                lambda _: self.handler_edit_user_story_request(user_story))

    def cancel_user_story_form(self):
        self.view.show_user_stories_list()

    def delete_user_story(self):
        user_story = self.view.user_stories.widget.get_focus().user_story

        uss_delete_f = self.executor.delete_user_story(user_story)
        uss_delete_f.add_done_callback(self.handler_delete_user_story_response)

    def move_current_us_up(self):
        current_focus = self.user_stories.index(self.view.user_stories.widget.get_focus().user_story)

        if current_focus > 0 and len(self.user_stories) > 2:
            current_us = self.user_stories[current_focus]
            self.user_stories[current_focus] = self.user_stories[current_focus - 1]
            self.user_stories[current_focus - 1] = current_us

            self.view.notifier.info_msg("Moved User story #{} up".format(current_us["ref"]))

            self.view.user_stories.populate(self.user_stories, self.project_stats, set_focus=current_us)

    def move_current_us_down(self):
        current_focus = self.user_stories.index(self.view.user_stories.widget.get_focus().user_story)

        if current_focus < len(self.user_stories) - 1 and len(self.user_stories) > 2:
            current_us = self.user_stories[current_focus]
            self.user_stories[current_focus] = self.user_stories[current_focus + 1]
            self.user_stories[current_focus + 1] = current_us

            self.view.notifier.info_msg("Moved User story #{} down".format(current_us["ref"]))

            self.view.user_stories.populate(self.user_stories, self.project_stats, set_focus=current_us)

    def update_user_stories_order(self):
        uss_post_f = self.executor.update_user_stories_order(self.user_stories, self.view.project)
        uss_post_f.add_done_callback(self.handler_update_user_stories_order_response)

    def handle_project_stats(self, future):
        self.project_stats = future.result()

    def handle_user_stories(self, future):
        self.user_stories = future.result()

    def when_backlog_info_fetched(self, future_with_results, info_msg=None, error_msg=None):
        done, not_done = future_with_results.result()

        if len(done) == 2:
            # FIXME TODO: Moved to handle_project_stats and fixed populate method tu update the content
            #             of the main widget instead of replace the widget
            if self.project_stats is not None:
                self.view.stats.populate(self.project_stats)

            self.view.user_stories.populate(self.user_stories, self.project_stats)
            if info_msg:
                self.view.notifier.info_msg(info_msg) #
            self.state_machine.refresh()
        else:
            # TODO retry failed operationsi
            if error_msg:
                self.view.notifier.error_msg(error_msg)

    def handler_create_user_story_request(self):
        data = self.view.get_user_story_form_data()

        if not data.get("subject", None):
            self.view.notifier.error_msg("Subject is required")
        else:
            us_post_f = self.executor.create_user_story(data)
            us_post_f.add_done_callback(self.handler_create_user_story_response)

    def handler_create_user_story_response(self, future):
        response = future.result()

        if response is None:
            self.view.notifier.error_msg("Create error")
        else:
            self.view.notifier.info_msg("Create succesful!")
            self.view.show_user_stories_list()

            project_stats_f = self.executor.project_stats(self.view.project)
            project_stats_f.add_done_callback(self.handle_project_stats)

            user_stories_f = self.executor.unassigned_user_stories(self.view.project)
            user_stories_f.add_done_callback(self.handle_user_stories)

            futures = (project_stats_f, user_stories_f)
            futures_completed_f = self.executor.pool.submit(lambda : wait(futures, 10))
            futures_completed_f.add_done_callback(functools.partial(self.when_backlog_info_fetched))

    def handler_edit_user_story_request(self, user_story):
        data = self.view.get_user_story_form_data()

        if not data.get("subject", None):
            self.view.notifier.error_msg("Subject is required")
        else:
            us_patch_f = self.executor.update_user_story(user_story, data)
            us_patch_f.add_done_callback(self.handler_edit_user_story_response)

    def handler_edit_user_story_response(self, future):
        response = future.result()

        if response is None:
            self.view.notifier.error_msg("Edit error")
        else:
            self.view.notifier.info_msg("Edit succesful!")
            self.view.show_user_stories_list()

            project_stats_f = self.executor.project_stats(self.view.project)
            project_stats_f.add_done_callback(self.handle_project_stats)

            user_stories_f = self.executor.unassigned_user_stories(self.view.project)
            user_stories_f.add_done_callback(self.handle_user_stories)

            futures = (project_stats_f, user_stories_f)
            futures_completed_f = self.executor.pool.submit(lambda : wait(futures, 10))
            futures_completed_f.add_done_callback(functools.partial(self.when_backlog_info_fetched))

    def handler_delete_user_story_response(self, future):
        response = future.result()

        if response is None:
            self.view.notifier.error_msg("Error deleting user_story")

            user_stories_f = self.executor.unassigned_user_stories(self.view.project)
            user_stories_f.add_done_callback(self.handle_user_stories)
        else:
            self.view.notifier.info_msg("Delete user story")

            project_stats_f = self.executor.project_stats(self.view.project)
            project_stats_f.add_done_callback(self.handle_project_stats)

            user_stories_f = self.executor.unassigned_user_stories(self.view.project)
            user_stories_f.add_done_callback(self.handle_user_stories)

            futures = (project_stats_f, user_stories_f)
            futures_completed_f = self.executor.pool.submit(lambda : wait(futures, 10))
            futures_completed_f.add_done_callback(functools.partial(self.when_backlog_info_fetched))

    def handler_update_user_stories_order_response(self, future):
        response = future.result()

        if response is None:
            self.view.notifier.error_msg("Error moving user_story")

            user_stories_f = self.executor.unassigned_user_stories(self.view.project)
            user_stories_f.add_done_callback(self.handle_user_stories)
        else:
            self.view.notifier.info_msg("Save  user stories")

            project_stats_f = self.executor.project_stats(self.view.project)
            project_stats_f.add_done_callback(self.handle_project_stats)

            user_stories_f = self.executor.unassigned_user_stories(self.view.project)
            user_stories_f.add_done_callback(self.handle_user_stories)

            futures = (project_stats_f, user_stories_f)
            futures_completed_f = self.executor.pool.submit(lambda : wait(futures, 10))
            futures_completed_f.add_done_callback(functools.partial(self.when_backlog_info_fetched))
