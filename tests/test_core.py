from unittest import mock

from gmncurses.config import Configuration
from gmncurses.core import GreenMineCore, StateMachine
from gmncurses import controllers

from . import factories


def test_if_client_is_not_authenticated_the_login_view_is_shown_on_startup():
    client = mock.Mock()
    client.is_authenticated = False
    configuration = Configuration()
    core = GreenMineCore(client, configuration)
    assert isinstance(core.controller, controllers.LoginController)
    assert core.state_machine.state == StateMachine.LOGIN

def test_if_client_is_authenticated_the_projects_view_is_shown_on_startup():
    client = mock.Mock()
    client.is_authenticated = True
    client.get_projects = mock.Mock(return_value=[])
    configuration = Configuration()
    core = GreenMineCore(client, configuration)
    assert isinstance(core.controller, controllers.ProjectsController)
    assert core.state_machine.state == StateMachine.PROJECTS

def test_transitioning_from_projects_to_project_detail():
    client = mock.Mock()
    client.get_project = mock.Mock(return_value=factories.project())
    client.is_authenticated = True
    projects = factories.projects()
    client.get_projects = mock.Mock(return_value=projects)
    configuration = Configuration()
    core = GreenMineCore(client, configuration)
    setattr(core, "transition", mock.Mock())
    assert isinstance(core.controller, controllers.ProjectsController)
    assert core.state_machine.state == StateMachine.PROJECTS
    core.state_machine.project_detail(projects[0])
    assert isinstance(core.controller, controllers.ProjectDetailController)
    assert core.state_machine.state == StateMachine.PROJECT_DETAIL


