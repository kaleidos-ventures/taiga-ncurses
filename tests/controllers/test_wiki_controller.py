from concurrent.futures import Future
from unittest import mock

from taiga_ncurses.ui import signals, views
from taiga_ncurses import controllers, config
from taiga_ncurses.executor import Executor
from taiga_ncurses.core import StateMachine

from tests import factories


