from concurrent.futures import Future
from unittest import mock

from gmncurses.ui import signals, views
from gmncurses import controllers, config
from gmncurses.executor import Executor
from gmncurses.core import StateMachine

from tests import factories


def test_sprints_controller_show_the_help_popup():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(config.ProjectKeys.MILESTONES)

    assert not hasattr(project_detail_controller.view.sprint, "help_popup")
    project_detail_controller.handle(config.ProjectMilestoneKeys.HELP)
    assert hasattr(project_detail_controller.view.sprint, "help_popup")

def test_sprints_controller_close_the_help_popup():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(config.ProjectKeys.MILESTONES)
    project_detail_controller.handle(config.ProjectMilestoneKeys.HELP)

    assert hasattr(project_detail_controller.view.sprint, "help_popup")
    help_popup = project_detail_controller.view.sprint.help_popup
    signals.emit(help_popup.close_button, "click")
    assert not hasattr(project_detail_controller.view.sprint, "help_popup")

def test_sprints_controller_reload():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(config.ProjectKeys.MILESTONES)
    executor.milestone.reset_mock()
    executor.milestone_stats.reset_mock()
    executor.user_stories.reset_mock()
    executor.milestone_tasks.reset_mock()

    assert executor.milestone.call_count == 0
    assert executor.milestone_stats.call_count == 0
    assert executor.user_stories.call_count == 0
    assert executor.milestone_tasks.call_count == 0
    project_detail_controller.handle(config.ProjectMilestoneKeys.RELOAD)
    assert executor.milestone.call_count == 1
    assert executor.milestone_stats.call_count == 1
    assert executor.user_stories.call_count == 1
    assert executor.milestone_tasks.call_count == 1
