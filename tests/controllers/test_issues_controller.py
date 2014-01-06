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
