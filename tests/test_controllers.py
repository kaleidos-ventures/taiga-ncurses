from concurrent.futures import Future
from unittest import mock

from gmncurses.ui import signals, views
from gmncurses import controllers
from gmncurses.executor import Executor
from gmncurses.core import StateMachine

from . import factories


def test_when_clicking_login_button_controllers_handle_login_method_is_called():
    login_view = factories.login_view("", "")
    _ = mock.Mock()
    login_controller = controllers.LoginController(login_view, _, _)
    login_controller.handle_login_request = mock.Mock()
    signals.emit(login_view.login_button, "click")
    assert login_controller.handle_login_request.call_count == 1

def test_login_controller_prints_an_error_message_on_unsuccessful_login():
    login_view = factories.login_view("admin", "123123")
    login_view.notifier = mock.Mock()
    executor = factories.patched_executor(login_response=factories.future(None))
    _ = mock.Mock()
    login_controller = controllers.LoginController(login_view, executor, _)

    signals.emit(login_view.login_button, "click")

    assert login_view.notifier.error_msg.call_count == 1

def test_login_controller_transitions_to_projects_on_successful_login():
    username, password = "admin", "123123"
    login_view = factories.login_view(username, password)

    resp = Future()
    resp.set_result(factories.successful_login_response(username))
    f = mock.Mock()
    f.add_done_callback = lambda f: f(resp)
    executor  = mock.Mock()
    executor.login = mock.Mock(return_value=f)
    state_machine = mock.Mock()
    login_controller = controllers.LoginController(login_view, executor, state_machine)

    signals.emit(login_view.login_button, "click")

    assert state_machine.logged_in.call_count == 1

def test_projects_controller_click_on_project_requests_the_project_detail():
    projects = factories.projects()
    projects_view = views.ProjectsView()
    executor = factories.patched_executor()
    _ = mock.Mock()
    projects_controller = controllers.ProjectsController(projects_view, executor, _)

    signals.emit(projects_view.project_buttons[0], "click")

    executor.project_detail.assert_called_with(projects[0])

def test_projects_controller_when_requesting_a_project_info_message_is_shown():
    projects = factories.projects()
    projects_view = views.ProjectsView()
    projects_view.notifier = mock.Mock()
    executor = factories.patched_executor()
    _ = mock.Mock()
    projects_controller = controllers.ProjectsController(projects_view, executor, _)

    signals.emit(projects_view.project_buttons[0], "click")

    assert projects_view.notifier.info_msg.call_count == 1

def test_projects_controller_click_on_project_when_project_is_fetched_transitions_to_project_detail():
    projects = factories.projects()
    fetched_project = projects[0]
    projects_view = views.ProjectsView()
    executor = factories.patched_executor(project_detail=factories.future(fetched_project))
    state_machine = mock.Mock()
    projects_controller = controllers.ProjectsController(projects_view, executor, state_machine)

    signals.emit(projects_view.project_buttons[0], "click")

    state_machine.project_detail.assert_called_with(fetched_project)

def test_projects_controller_when_project_fetching_fails_a_error_message_is_shown():
    projects = factories.projects()
    fetched_project = projects[0]
    projects_view = views.ProjectsView()
    projects_view.notifier = mock.Mock()
    executor = factories.patched_executor(project_detail=factories.future(None))
    _ = mock.Mock()
    projects_controller = controllers.ProjectsController(projects_view, executor, _)

    signals.emit(projects_view.project_buttons[0], "click")

    assert projects_view.notifier.error_msg.call_count == 1

def test_project_detail_controller_fetches_user_stories_and_transitions_to_backlog():
    project = factories.project()
    project_view = views.ProjectDetailView(project)
    executor = factories.patched_executor()
    state_machine = StateMachine(mock.Mock(), StateMachine.PROJECTS)
    project_detail_controller = controllers.ProjectDetailController(project_view, executor, state_machine)

    assert state_machine.state == state_machine.PROJECT_BACKLOG
