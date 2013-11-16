# -*- coding: utf-8 -*-

"""
gmncurses.cli
~~~~~~~~~~~~~

"""

from gmncurses.api.client import GreenMineClient
from gmncurses.core import GreenMineCore
from gmncurses.config import GREENMINE_HOST


def main():
    gm = GreenMineClient(GREENMINE_HOST)
    program = GreenMineCore(gm)
    program.run()
