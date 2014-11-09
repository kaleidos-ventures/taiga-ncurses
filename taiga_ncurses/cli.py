# -*- coding: utf-8 -*-

"""
taiga_ncurses.cli
~~~~~~~~~~~~~~~~~
"""

from taiga_ncurses.api.client import TaigaClient
from taiga_ncurses.core import TaigaCore
from taiga_ncurses.config import settings
from taiga_ncurses.executor import Executor


def main():
    settings.load()
    client = TaigaClient(settings.host)
    if settings.data.auth.token:
        client.set_auth_token(settings.data.auth.token)
    executor = Executor(client)
    program = TaigaCore(executor, settings, authenticated=settings.data.auth.token)
    program.run()
