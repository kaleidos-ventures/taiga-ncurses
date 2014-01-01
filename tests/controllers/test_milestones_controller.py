from concurrent.futures import Future
from unittest import mock

from gmncurses.ui import signals, views
from gmncurses import controllers, config
from gmncurses.executor import Executor
from gmncurses.core import StateMachine

from tests import factories


def test_project_detail_sprints_controller_show_the_help_popup():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(config.ProjectKeys.MILESTONES)

    assert not hasattr(project_detail_controller.view.sprint, "help_popup")
    project_detail_controller.handle(config.ProjectMilestoneKeys.HELP)
    assert hasattr(project_detail_controller.view.sprint, "help_popup")
