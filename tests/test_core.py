from unittest import mock

from gmncurses.config import Configuration
from gmncurses.core import GreenMineCore
from gmncurses import controllers


def test_if_client_is_not_authenticated_the_login_view_is_shown_on_startup():
    client = mock.Mock()
    client.is_authenticated = False
    configuration = Configuration()
    core = GreenMineCore(client, configuration)
    assert isinstance(core.controller, controllers.LoginController)

def test_if_client_is_authenticated_the_projects_view_is_shown_on_startup():
    client = mock.Mock()
    client.is_authenticated = True
    client.get_projects = mock.Mock(return_value=[])
    configuration = Configuration()
    core = GreenMineCore(client, configuration)
    assert isinstance(core.controller, controllers.ProjectsController)
