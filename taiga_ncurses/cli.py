# -*- coding: utf-8 -*-

"""
taiga_ncurses.cli
~~~~~~~~~~~~~
"""

from taiga_ncurses.api.client import TaigaClient
from taiga_ncurses.core import TaigaCore
from taiga_ncurses.config import settings
from taiga_ncurses.executor import Executor


def main():
    settings.load()
    client = TaigaClient(settings.host)
    if settings.auth_token:
        client.set_auth_token(settings.auth_token)
    executor = Executor(client)
    program = TaigaCore(executor, settings, authenticated=settings.auth_token)
    program.run()
