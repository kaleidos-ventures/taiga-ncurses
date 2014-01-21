# -*- coding: utf-8 -*-

"""
gmncurses.cli
~~~~~~~~~~~~~
"""

from gmncurses.api.client import TaigaClient
from gmncurses.core import TaigaCore
from gmncurses.config import Configuration, DEFAULTS
from gmncurses.executor import Executor


def main():
    config = Configuration()
    config.load()
    client = TaigaClient(config.host)
    if config.auth_token:
        client.set_auth_token(config.auth_token)
    executor = Executor(client)
    program = TaigaCore(executor, config, authenticated=config.auth_token)
    program.run()
