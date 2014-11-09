# -*- coding: utf-8 -*-

"""
taiga_ncurses.controllers.backlog
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from concurrent.futures import wait
import functools, copy

from taiga_ncurses.config import settings
from taiga_ncurses.ui import signals

from . import base


class ProjectBacklogSubController(base.Controller):
    def __init__(self, view, executor, state_machine):
        self.view = view
        self.executor = executor
        self.state_machine = state_machine

        self.view.user_stories.on_user_story_status_change = self.handle_change_user_story_status_request
        self.view.user_stories.on_user_story_points_change = self.handle_change_user_story_points_request

    def handle(self, key):
        if key == settings.data.backlog.keys.create:
            self.new_user_story()
        if key == settings.data.backlog.keys.create_in_bulk:
            self.new_user_stories_in_bulk()
        elif key == settings.data.backlog.keys.edit:
            self.edit_user_story()
        elif key == settings.data.backlog.keys.delete:
            self.delete_user_story()
        elif key == settings.data.backlog.keys.increase_priority:
            self.move_current_us_up()
        elif key == settings.data.backlog.keys.decrease_priority:
            self.move_current_us_down()
        elif key == settings.data.backlog.keys.update_order:
            self.update_user_stories_order()
        elif key == settings.data.backlog.keys.move_to_milestone:
            self.move_user_story_to_milestone()
        elif key == settings.data.backlog.keys.reload:
            self.load()
        elif key == settings.data.backlog.keys.help:
            self.help_info()
        else:
            super().handle(key)

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
        self.view.close_user_story_form()

    def new_user_stories_in_bulk(self):
        self.view.open_user_stories_in_bulk_form()

        signals.connect(self.view.user_stories_in_bulk_form.cancel_button, "click",
                lambda _: self.cancel_user_stories_in_bulk_form())
        signals.connect(self.view.user_stories_in_bulk_form.save_button, "click",
                lambda _: self.handler_create_user_stories_in_bulk_request())

    def cancel_user_stories_in_bulk_form(self):
        self.view.close_user_stories_in_bulk_form()

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

    def move_user_story_to_milestone(self):
        user_story = self.view.user_stories.widget.get_focus().user_story
        self.view.open_milestones_selector_popup(user_story=user_story)

        signals.connect(self.view.milestone_selector_popup.cancel_button, "click",
                        lambda _: self.cancel_milestone_selector_popup())

        for option in self.view.milestone_selector_popup.options:
            signals.connect(option, "click", functools.partial(
                    self.handler_move_user_story_to_milestone_request, user_story=user_story))

    def cancel_milestone_selector_popup(self):
        self.view.close_milestone_selector_popup()

    def help_info(self):
        self.view.open_help_popup()

        signals.connect(self.view.help_popup.close_button, "click",
                lambda _: self.close_help_info())

    def close_help_info(self):
        self.view.close_help_popup()

    def handle_project_stats(self, future):
        self.project_stats = future.result()

    def handle_user_stories(self, future):
        self.user_stories = future.result()

    def when_backlog_info_fetched(self, future_with_results, info_msg=None, error_msg=None):
        done, not_done = future_with_results.result()

        if len(done) == 2:
            # FIXME TODO: Moved to handle_project_stats and fixed populate method to update the content
            #             of the main widget instead of replace the widget
            self.view.stats.populate(self.project_stats)
            self.view.user_stories.populate(self.user_stories, self.project_stats)

            if info_msg:
                self.view.notifier.info_msg(info_msg)

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
            self.view.notifier.info_msg("Create successful!")
            self.view.close_user_story_form()

            project_stats_f = self.executor.project_stats(self.view.project)
            project_stats_f.add_done_callback(self.handle_project_stats)

            user_stories_f = self.executor.unassigned_user_stories(self.view.project)
            user_stories_f.add_done_callback(self.handle_user_stories)

            futures = (project_stats_f, user_stories_f)
            futures_completed_f = self.executor.pool.submit(lambda : wait(futures, 10))
            futures_completed_f.add_done_callback(self.when_backlog_info_fetched)

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
            self.view.notifier.info_msg("Edit successful!")
            self.view.close_user_story_form()

            project_stats_f = self.executor.project_stats(self.view.project)
            project_stats_f.add_done_callback(self.handle_project_stats)

            user_stories_f = self.executor.unassigned_user_stories(self.view.project)
            user_stories_f.add_done_callback(self.handle_user_stories)

            futures = (project_stats_f, user_stories_f)
            futures_completed_f = self.executor.pool.submit(lambda : wait(futures, 10))
            futures_completed_f.add_done_callback(self.when_backlog_info_fetched)

    def handler_create_user_stories_in_bulk_request(self):
        data = self.view.get_user_stories_in_bulk_form_data()

        if not data.get("bulkStories", None):
            self.view.notifier.error_msg("Subjects are required")
        else:
            us_post_f = self.executor.create_user_stories_in_bulk(data)
            us_post_f.add_done_callback(self.handler_create_user_stories_in_bulk_response)

    def handler_create_user_stories_in_bulk_response(self, future):
        response = future.result()

        if response is None:
            self.view.notifier.error_msg("Create error")
        else:
            self.view.notifier.info_msg("Create successful!")
            self.view.close_user_stories_in_bulk_form()

            project_stats_f = self.executor.project_stats(self.view.project)
            project_stats_f.add_done_callback(self.handle_project_stats)

            user_stories_f = self.executor.unassigned_user_stories(self.view.project)
            user_stories_f.add_done_callback(self.handle_user_stories)

            futures = (project_stats_f, user_stories_f)
            futures_completed_f = self.executor.pool.submit(lambda : wait(futures, 10))
            futures_completed_f.add_done_callback(self.when_backlog_info_fetched)

    def handler_delete_user_story_response(self, future):
        response = future.result()

        if response is None:
            self.view.notifier.error_msg("Error deleting user_story")
        else:
            self.view.notifier.info_msg("Delete user story")

            project_stats_f = self.executor.project_stats(self.view.project)
            project_stats_f.add_done_callback(self.handle_project_stats)

            user_stories_f = self.executor.unassigned_user_stories(self.view.project)
            user_stories_f.add_done_callback(self.handle_user_stories)

            futures = (project_stats_f, user_stories_f)
            futures_completed_f = self.executor.pool.submit(lambda : wait(futures, 10))
            futures_completed_f.add_done_callback(self.when_backlog_info_fetched)

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
            futures_completed_f.add_done_callback(self.when_backlog_info_fetched)

    def handler_move_user_story_to_milestone_request(self, selected_option, user_story=None):
        data = {"milestone": selected_option.milestone["id"]}

        us_patch_f = self.executor.update_user_story(user_story, data)
        us_patch_f.add_done_callback(self.handler_move_user_story_to_milestone_response)

        self.cancel_milestone_selector_popup()

    def handler_move_user_story_to_milestone_response(self, future):
        response = future.result()

        if response is None:
            self.view.notifier.error_msg("Error moving user story to milestone")
        else:
            self.view.notifier.info_msg("Moved user story to milestone succesful!")

            project_stats_f = self.executor.project_stats(self.view.project)
            project_stats_f.add_done_callback(self.handle_project_stats)

            user_stories_f = self.executor.unassigned_user_stories(self.view.project)
            user_stories_f.add_done_callback(self.handle_user_stories)

            futures = (project_stats_f, user_stories_f)
            futures_completed_f = self.executor.pool.submit(lambda : wait(futures, 10))
            futures_completed_f.add_done_callback(self.when_backlog_info_fetched)

    def handle_change_user_story_status_request(self, combo, item, state, user_data=None):
        data = {"status": item.value}
        user_story = user_data

        user_story_patch_f = self.executor.update_user_story(user_story, data)
        user_story_patch_f.add_done_callback(self.handle_change_user_story_status_response)

    def handle_change_user_story_status_response(self, future):
        response = future.result()

        if response is None:
            self.view.notifier.error_msg("Change user story status with errors")
            # TODO: Select old value
        else:
            self.view.notifier.info_msg("Change user story status successful!")

            project_stats_f = self.executor.project_stats(self.view.project)
            project_stats_f.add_done_callback(self.handle_project_stats)

            user_stories_f = self.executor.unassigned_user_stories(self.view.project)
            user_stories_f.add_done_callback(self.handle_user_stories)

            futures = (project_stats_f, user_stories_f)
            futures_completed_f = self.executor.pool.submit(lambda : wait(futures, 10))
            futures_completed_f.add_done_callback(self.when_backlog_info_fetched)

    def handle_change_user_story_points_request(self, combo, item, state, user_data=None):
        user_story, role_id = user_data
        data = {"points": {role_id: item.value}}

        user_story_patch_f = self.executor.update_user_story(user_story, data)
        user_story_patch_f.add_done_callback(self.handle_change_user_story_points_response)

    def handle_change_user_story_points_response(self, future):
        response = future.result()

        if response is None:
            self.view.notifier.error_msg("Change user story points with errors")
            # TODO: Select old value
        else:
            self.view.notifier.info_msg("Change user story points successful!")

            project_stats_f = self.executor.project_stats(self.view.project)
            project_stats_f.add_done_callback(self.handle_project_stats)

            user_stories_f = self.executor.unassigned_user_stories(self.view.project)
            user_stories_f.add_done_callback(self.handle_user_stories)

            futures = (project_stats_f, user_stories_f)
            futures_completed_f = self.executor.pool.submit(lambda : wait(futures, 10))
            futures_completed_f.add_done_callback(self.when_backlog_info_fetched)
