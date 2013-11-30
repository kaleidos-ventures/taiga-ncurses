# -*- coding: utf-8 -*-

"""
gmncurses.config
~~~~~~~~~~~~~~~~
"""

import urllib


PALETTE = [
    ('green', 'dark green', 'default'),
    ('green-bg', 'white', 'dark green'),
    ('editor', 'white', 'black'),
    ('password-editor', 'light red', 'black'),
    ('save-button', 'white', 'default'),
    ('error', 'white', 'dark red'),
    ('info', 'white', 'dark blue'),
]

class KeyConfigMeta(type):
    def __new__(cls, clsname, bases, dct):
        dct['config'] = {v: k.capitalize().replace('_', ' ') for k, v in dct.items() if k.isupper()}
        return super().__new__(cls, clsname, bases, dct)


class Keys(metaclass=KeyConfigMeta):
    QUIT = 'q'
    DEBUG = 'D'


DEFAULTS = {
    'keys': Keys.config,
    'host': {
        'protocol': 'http',
        'url': 'api.greenmine.kaleidos.net',
    },
}

class Configuration(object):
    def __init__(self, configdict):
        self.configdict = configdict

    @property
    def host(self):
        host = self.configdict['host']
        assert host['protocol'] in ('http', 'https')
        return "{protocol}://{url}".format(protocol=host['protocol'],
                                           url=urllib.parse.quote(host['url']))

