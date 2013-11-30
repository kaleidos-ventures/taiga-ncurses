from unittest import mock
from concurrent.futures import Future

from gmncurses import executor


def test_login_method_returns_a_future():
    client = mock.Mock()
    c = executor.Executor(client)
    f = c.login("admin", "123123")
    assert isinstance(f, Future)
