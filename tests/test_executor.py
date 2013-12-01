from unittest import mock
from concurrent.futures import Future

from gmncurses import executor


def test_login_method_returns_a_future():
    client = mock.Mock()
    e = executor.Executor(client)
    f = e.login("admin", "123123")
    assert isinstance(f, Future)

def test_project_detail_method_returns_a_future():
    client = mock.Mock()
    e = executor.Executor(client)
    f = e.project_detail({"id": 123123})
    assert isinstance(f, Future)

def test_user_stories_method_returns_a_future():
    client = mock.Mock()
    e = executor.Executor(client)
    f = e.user_stories({"id": 123123})
    assert isinstance(f, Future)
