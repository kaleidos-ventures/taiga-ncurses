# -*- coding: utf-8 -*-

"""
gmncurses.cli
~~~~~~~~~~~~~
"""

from gmncurses.api.client import GreenMineClient
from gmncurses.core import GreenMineCore
from gmncurses.config import Configuration, DEFAULTS
from gmncurses.executor import Executor


def main():
    config = Configuration()
    config.load()
    client = GreenMineClient(config.host)
    if config.auth_token:
        client.set_auth_token(config.auth_token)
    executor = Executor(client)
    program = GreenMineCore(executor, config, authenticated=config.auth_token)
    program.run()
