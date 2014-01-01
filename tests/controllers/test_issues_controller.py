from concurrent.futures import Future
from unittest import mock

from gmncurses.ui import signals, views
from gmncurses import controllers, config
from gmncurses.executor import Executor
from gmncurses.core import StateMachine

from tests import factories


def test_project_detail_issues_controller_show_the_help_popup():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(config.ProjectKeys.ISSUES)

    assert not hasattr(project_detail_controller.view.issues, "help_popup")
    project_detail_controller.handle(config.ProjectIssuesKeys.HELP)
    assert hasattr(project_detail_controller.view.issues, "help_popup")
