# -*- coding: utf-8 -*-

"""
gmncurses.cli
~~~~~~~~~~~~~

"""

from gmncurses.api.client import GreenMineClient
from gmncurses.core import GreenMineCore
from gmncurses.config import Configuration, DEFAULTS


def main():
    config = Configuration(DEFAULTS)
    gm = GreenMineClient(config.host)
    program = GreenMineCore(gm)
    program.run()
