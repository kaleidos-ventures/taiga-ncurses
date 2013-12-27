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
        if key == ProjectIssuesKeys.RELOAD:
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

        issues_f = self.executor.issues(self.view.project)
        issues_f.add_done_callback(self.handle_issues)

        futures = (issues_stats_f, issues_f)
        futures_completed_f = self.executor.pool.submit(lambda : wait(futures, 10))
        futures_completed_f.add_done_callback(self.when_issues_info_fetched)

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
                    functools.partial(self.order_by, "issue"))

            signals.connect(self.view.issues.header.status_button, "click",
                    functools.partial(self.order_by, "status"))

            signals.connect(self.view.issues.header.priority_button, "click",
                    functools.partial(self.order_by, "priority"))

            signals.connect(self.view.issues.header.severity_buttton, "click",
                    functools.partial(self.order_by, "severity"))

            signals.connect(self.view.issues.header.assigned_to_button, "click",
                    functools.partial(self.order_by, "assigned_to"))

            self.state_machine.refresh()

    def when_issues_info_fetched(self, future_with_results):
        done, not_done = future_with_results.result()
        if len(done) == 2:
            self.view.notifier.info_msg("Stats and issues fetched")
            self.state_machine.refresh()
        else:
            # TODO retry failed operations
            self.view.notifier.error_msg("Failed to fetch issues data")

    def order_by(self, param, button):
        self.view.notifier.info_msg("Ordered issues by {}".format(param))
        issues_f = self.executor.issues(self.view.project, order_by=[param])
        issues_f.add_done_callback(self.handle_refresh_issues)

    def handle_refresh_issues(self, future):
        self.issues = future.result()
        if self.issues is not None:
            self.view.issues.populate(self.issues)
            self.state_machine.refresh()


