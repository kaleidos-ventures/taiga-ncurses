from concurrent.futures import Future
from unittest import mock

from gmncurses.ui import signals, views
from gmncurses import controllers, config
from gmncurses.executor import Executor
from gmncurses.core import StateMachine

from tests import factories


def test_issues_controller_show_the_filters_popup():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(config.ProjectKeys.ISSUES)

    assert not hasattr(project_detail_controller.view.issues, "filters_popup")
    project_detail_controller.handle(config.ProjectIssuesKeys.FILTERS)
    assert hasattr(project_detail_controller.view.issues, "filters_popup")

def test_issues_controller_submit_the_filters_popup():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.issues.notifier = mock.Mock()
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(config.ProjectKeys.ISSUES)
    project_detail_controller.handle(config.ProjectIssuesKeys.FILTERS)
    filters_popup = project_detail_controller.view.issues.filters_popup
    project_view.issues.notifier.reset_mock()
    executor.issues.reset_mock()

    assert project_view.issues.notifier.info_msg.call_count == 0
    assert executor.issues.call_count == 0
    filters_popup._issue_types_group[0].set_state(True)
    filters_popup._issue_statuses_group[0].set_state(True)
    filters_popup._priorities_group[0].set_state(True)
    filters_popup._severities_group[0].set_state(True)
    filters_popup._assigned_to_group[0].set_state(True)
    filters_popup._created_by_group[0].set_state(True)
    #filters_popup._tags_group[0].set_state(True)
    signals.emit(filters_popup.filter_button, "click")
    assert project_view.issues.notifier.info_msg.call_count == 1
    assert executor.issues.call_count == 1
    assert len(filters_popup._filters) == 7
    assert len(executor.issues.call_args.call_list()[0][1]["filters"]["type"]) == 1
    assert len(executor.issues.call_args.call_list()[0][1]["filters"]["status"]) == 1
    assert len(executor.issues.call_args.call_list()[0][1]["filters"]["severity"]) == 1
    assert len(executor.issues.call_args.call_list()[0][1]["filters"]["priority"]) == 1
    assert len(executor.issues.call_args.call_list()[0][1]["filters"]["assigned_to"]) == 1
    assert len(executor.issues.call_args.call_list()[0][1]["filters"]["owner"]) == 1
    #assert len(executor.issues.call_args.call_list()[0][1]["filters"]["tags"]) == 1

def test_issues_controller_cancel_the_filters_popup():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(config.ProjectKeys.ISSUES)
    project_detail_controller.handle(config.ProjectIssuesKeys.FILTERS)

    assert hasattr(project_detail_controller.view.issues, "filters_popup")
    filters_popup = project_detail_controller.view.issues.filters_popup
    signals.emit(filters_popup.cancel_button, "click")
    assert not hasattr(project_detail_controller.view.issues, "filters_popup")

def test_issues_controller_show_the_help_popup():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(config.ProjectKeys.ISSUES)

    assert not hasattr(project_detail_controller.view.issues, "help_popup")
    project_detail_controller.handle(config.ProjectIssuesKeys.HELP)
    assert hasattr(project_detail_controller.view.issues, "help_popup")

def test_issues_controller_close_the_help_popup():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(config.ProjectKeys.ISSUES)
    project_detail_controller.handle(config.ProjectIssuesKeys.HELP)

    assert hasattr(project_detail_controller.view.issues, "help_popup")
    help_popup = project_detail_controller.view.issues.help_popup
    signals.emit(help_popup.close_button, "click")
    assert not hasattr(project_detail_controller.view.issues, "help_popup")

def test_issues_controller_reload():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(config.ProjectKeys.ISSUES)
    executor.project_issues_stats.reset_mock()
    executor.issues.reset_mock()

    assert executor.project_issues_stats.call_count == 0
    assert executor.issues.call_count == 0
    project_detail_controller.handle(config.ProjectIssuesKeys.RELOAD)
    assert executor.project_issues_stats.call_count == 1
    assert executor.issues.call_count == 1
