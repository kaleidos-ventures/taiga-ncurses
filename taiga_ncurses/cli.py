# -*- coding: utf-8 -*-

"""
taiga_ncurses.cli
~~~~~~~~~~~~~
"""

from taiga_ncurses.api.client import TaigaClient
from taiga_ncurses.core import TaigaCore
from taiga_ncurses.config import Configuration, DEFAULTS
from taiga_ncurses.executor import Executor


def main():
    config = Configuration()
    config.load()
    client = TaigaClient(config.host)
    if config.auth_token:
        client.set_auth_token(config.auth_token)
    executor = Executor(client)
    program = TaigaCore(executor, config, authenticated=config.auth_token)
    program.run()
