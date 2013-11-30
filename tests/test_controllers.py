from unittest import mock

from gmncurses.ui import signals
from gmncurses import controllers

from . import factories


def test_when_clicking_login_button_controllers_handle_login_method_is_called():
    login_view = factories.login_view("", "")
    _ = mock.Mock()
    login_controller = controllers.LoginController(login_view, _, _)
    login_controller.handle_login_request = mock.Mock()
    signals.emit(login_view.login_button, "click")
    assert login_controller.handle_login_request.call_count == 1

def test_login_controller_prints_an_error_message_on_unsuccessful_login():
    username, password = "admin", "123123"
    login_view = factories.login_view(username, password)
    login_view.notifier = mock.Mock()

    f = mock.Mock()
    f.add_done_callback = lambda f: f(False)
    executor  = mock.Mock()
    executor.login = mock.Mock(return_value=f)
    _ = mock.Mock()
    login_controller = controllers.LoginController(login_view, executor, _)

    signals.emit(login_view.login_button, "click")

    assert login_view.notifier.error_msg.call_count == 1


def test_login_controller_transitions_to_projects_on_successful_login():
    username, password = "admin", "123123"
    login_view = factories.login_view(username, password)

    f = mock.Mock()
    f.add_done_callback = lambda f: f(factories.api_successful_login_response(username))
    executor  = mock.Mock()
    executor.login = mock.Mock(return_value=f)
    state_machine = mock.Mock()
    login_controller = controllers.LoginController(login_view, executor, state_machine)

    signals.emit(login_view.login_button, "click")

    assert state_machine.logged_in.call_count == 1
