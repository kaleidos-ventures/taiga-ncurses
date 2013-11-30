from unittest import mock

from gmncurses.ui import views, signals
from gmncurses import controllers


def test_when_clicking_login_button_controllers_handle_login_method_is_called():
    _ = mock.Mock()
    login_view = views.LoginView("username", "password")
    login_controller = controllers.LoginController(_, login_view, _)
    login_controller.handle_login = mock.Mock()
    signals.emit(login_view.login_button, "click")
    assert login_controller.handle_login.call_count == 1
