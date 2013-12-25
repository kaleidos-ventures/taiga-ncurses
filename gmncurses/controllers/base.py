# -*- coding: utf-8 -*-

"""
gmncurses.controllers.base
~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


class Controller(object):
    view = None

    def handle(self, key):
        return key
