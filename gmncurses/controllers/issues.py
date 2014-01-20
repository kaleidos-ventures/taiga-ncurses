# -*- coding: utf-8 -*-

"""
gmncurses.controllers.issues
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from concurrent.futures import wait
import functools

from gmncurses.config import ProjectIssuesKeys
from gmncurses.ui import signals

from . import base


class ProjectIssuesSubController(base.Controller):
    def __init__(self, view, executor, state_machine):
        self.view = view
        self.executor = executor
        self.state_machine = state_machine

    def handle(self, key):
        if key == ProjectIssuesKeys.CREATE_ISSUE:
            self.new_issue()
        elif key == ProjectIssuesKeys.EDIT_ISSUE:
            self.edit_issue()
        elif key == ProjectIssuesKeys.DELETE_ISSUE:
            self.delete_issue()
        elif key == ProjectIssuesKeys.FILTERS:
            self.filters()
        elif key == ProjectIssuesKeys.RELOAD:
            self.load()
        elif key == ProjectIssuesKeys.HELP:
            self.help_info()
        else:
            super().handle(key)

    def load(self):
        self.state_machine.transition(self.state_machine.PROJECT_ISSUES)

        self.view.notifier.info_msg("Fetching Stats and Issues")

        issues_stats_f = self.executor.project_issues_stats(self.view.project)
        issues_stats_f.add_done_callback(self.handle_issues_stats)

        issues_f = self.executor.issues(self.view.project, filters=self.view.filters)
        issues_f.add_done_callback(self.handle_issues)

        futures = (issues_stats_f, issues_f)
        futures_completed_f = self.executor.pool.submit(lambda : wait(futures, 10))
        futures_completed_f.add_done_callback(functools.partial(self.when_issues_info_fetched,
                                                                info_msg="Stats and issues fetched",
                                                                error_msg="Failed to fetch issues data"))

    def new_issue(self):
        self.view.open_issue_form()

        signals.connect(self.view.issue_form.cancel_button, "click",
                lambda _: self.cancel_issue_form())
        signals.connect(self.view.issue_form.save_button, "click",
                lambda _: self.handler_create_issue_request())

    def edit_issue(self):
        issue = self.view.issues.widget.get_focus().issue
        self.view.open_issue_form(issue=issue)

        signals.connect(self.view.issue_form.cancel_button, "click",
                lambda _: self.cancel_issue_form())
        signals.connect(self.view.issue_form.save_button, "click",
                lambda _: self.handler_edit_issue_request(issue))

    def cancel_issue_form(self):
        self.view.close_issue_form()

    def delete_issue(self):
        issue = self.view.issues.widget.get_focus().issue

        issue_delete_f = self.executor.delete_issue(issue)
        issue_delete_f.add_done_callback(self.handler_delete_issue_response)

    def filters(self):
        self.view.open_filters_popup()

        signals.connect(self.view.filters_popup.filter_button, "click",
                lambda _: self.apply_filters_from_filters_popup())

        signals.connect(self.view.filters_popup.cancel_button, "click",
                lambda _: self.cancel_filters_popup())

    def apply_filters_from_filters_popup(self):
        self.view.set_filters(self.view.get_filters_popup_data())

        self.view.notifier.info_msg("Filter issues")
        self.cancel_filters_popup()

        issues_f = self.executor.issues(self.view.project, filters=self.view.filters)
        issues_f.add_done_callback(self.handle_refresh_issues)

    def cancel_filters_popup(self):
        self.view.close_filters_popup()

    def help_info(self):
        self.view.open_help_popup()

        signals.connect(self.view.help_popup.close_button, "click",
                lambda _: self.close_help_info())

    def close_help_info(self):
        self.view.close_help_popup()

    def handle_issues_stats(self, future):
        self.issues_stats = future.result()
        if self.issues_stats is not None:
            self.view.stats.populate(self.issues_stats)
            self.state_machine.refresh()

    def handle_issues(self, future):
        self.issues = future.result()
        if self.issues is not None:
            self.view.issues.populate(self.issues)

            signals.connect(self.view.issues.header.issue_button, "click",
                    functools.partial(self.handle_order_by, "issue"))

            signals.connect(self.view.issues.header.status_button, "click",
                    functools.partial(self.handle_order_by, "status"))

            signals.connect(self.view.issues.header.priority_button, "click",
                    functools.partial(self.handle_order_by, "priority"))

            signals.connect(self.view.issues.header.severity_buttton, "click",
                    functools.partial(self.handle_order_by, "severity"))

            signals.connect(self.view.issues.header.assigned_to_button, "click",
                    functools.partial(self.handle_order_by, "assigned_to"))

            self.state_machine.refresh()
    def handler_create_issue_request(self):
        data = self.view.get_issue_form_data()

        if not data.get("subject", None):
            self.view.notifier.error_msg("Subject is required")
        else:
            us_post_f = self.executor.create_issue(data)
            us_post_f.add_done_callback(self.handler_create_issue_response)

    def handler_create_issue_response(self, future):
        response = future.result()

        if response is None:
            self.view.notifier.error_msg("Create error")
        else:
            self.view.notifier.info_msg("Create successful!")
            self.view.close_issue_form()

            issues_stats_f = self.executor.project_issues_stats(self.view.project)
            issues_stats_f.add_done_callback(self.handle_issues_stats)

            issues_f = self.executor.issues(self.view.project, filters=self.view.filters)
            issues_f.add_done_callback(self.handle_issues)

            futures = (issues_stats_f, issues_f)
            futures_completed_f = self.executor.pool.submit(lambda : wait(futures, 10))
            futures_completed_f.add_done_callback(self.when_issues_info_fetched)

    def handler_edit_issue_request(self, issue):
        data = self.view.get_issue_form_data()

        if not data.get("subject", None):
            self.view.notifier.error_msg("Subject is required")
        else:
            issue_patch_f = self.executor.update_issue(issue, data)
            issue_patch_f.add_done_callback(self.handler_edit_issue_response)

    def handler_edit_issue_response(self, future):
        response = future.result()

        if response is None:
            self.view.notifier.error_msg("Edit error")
        else:
            self.view.notifier.info_msg("Edit successful!")
            self.view.close_issue_form()

            issues_stats_f = self.executor.project_issues_stats(self.view.project)
            issues_stats_f.add_done_callback(self.handle_issues_stats)

            issues_f = self.executor.issues(self.view.project, filters=self.view.filters)
            issues_f.add_done_callback(self.handle_issues)

            futures = (issues_stats_f, issues_f)
            futures_completed_f = self.executor.pool.submit(lambda : wait(futures, 10))
            futures_completed_f.add_done_callback(self.when_issues_info_fetched)

    def handler_delete_issue_response(self, future):
        response = future.result()

        if response is None:
            self.view.notifier.error_msg("Error deleting issue")
        else:
            self.view.notifier.info_msg("Delete issue")

            issues_stats_f = self.executor.project_issues_stats(self.view.project)
            issues_stats_f.add_done_callback(self.handle_issues_stats)

            issues_f = self.executor.issues(self.view.project, filters=self.view.filters)
            issues_f.add_done_callback(self.handle_issues)

            futures = (issues_stats_f, issues_f)
            futures_completed_f = self.executor.pool.submit(lambda : wait(futures, 10))
            futures_completed_f.add_done_callback(self.when_issues_info_fetched)

    def handle_order_by(self, param, button):
        self.view.notifier.info_msg("Ordered issues by {}".format(param))
        issues_f = self.executor.issues(self.view.project, order_by=[param], filters=self.view.filters)
        issues_f.add_done_callback(self.handle_refresh_issues)

    def handle_refresh_issues(self, future):
        self.issues = future.result()
        if self.issues is not None:
            self.view.issues.populate(self.issues)
            self.state_machine.refresh()

    def when_issues_info_fetched(self, future_with_results, info_msg=None, error_msg=None):
        done, not_done = future_with_results.result()
        if len(done) == 2:
            if info_msg:
                self.view.notifier.info_msg(info_msg)
            self.state_machine.refresh()
        else:
            # TODO retry failed operations
            if error_msg:
                self.view.notifier.error_msg(error_msg)


