# -*- coding: utf-8 -*-

"""
gmncurses.config
~~~~~~~~~~~~~~~~
"""

import os
import urllib
from configparser import ConfigParser


DEFAULT_CONFIG_DIR =  os.path.join(os.environ["HOME"], ".gmncurses")
DEFAULT_CONFIG_FILE = os.path.join(DEFAULT_CONFIG_DIR, "config.ini")
DEFAULT_AUTH_FILE = os.path.join(DEFAULT_CONFIG_DIR, "auth.ini")

PALETTE = [
    ("green", "dark green", "default"),
    ("green-bg", "white", "dark green"),
    ("editor", "white", "black"),
    ("password-editor", "light red", "black"),
    ("save-button", "white", "default"),
    ("error", "white", "dark red"),
    ("info", "white", "dark blue"),
]

class KeyConfigMeta(type):
    def __new__(cls, clsname, bases, dct):
        dct["config"] = {v: k.capitalize().replace("_", " ") for k, v in dct.items() if k.isupper()}
        return super().__new__(cls, clsname, bases, dct)


class Keys(metaclass=KeyConfigMeta):
    QUIT = "q"
    DEBUG = "D"

DEFAULTS = {
    "keys": Keys.config,
    "host": {
        "scheme": "http",
        "domain": "localhost",
        "port": "8000",
    },
}

class Configuration(object):
    def __init__(self,
                 config_dict=DEFAULTS,
                 config_file=DEFAULT_CONFIG_FILE,
                 auth_config_file=DEFAULT_AUTH_FILE):
        self.config_dict = config_dict
        self.config_file = config_file
        self.auth_config_file = auth_config_file

    def load(self):
        parser = ConfigParser()
        parser.read(self.config_file, encoding="utf-8")
        self.config_dict.update(parser._sections)
        auth_parser = ConfigParser()
        auth_parser.read(self.auth_config_file, encoding="utf-8")
        self.config_dict.update(auth_parser._sections)

    @property
    def host(self):
        host = self.config_dict["host"]

        scheme = host["scheme"]
        assert scheme in ("http", "https")
        domain = urllib.parse.quote(host["domain"])
        port = ":{}".format(host["port"]) if "port" in host else ""

        return "{scheme}://{domain}{port}".format(scheme=scheme, domain=domain, port=port)

    @property
    def auth_token(self):
        auth_dict = self.config_dict.get("auth", None)
        if auth_dict is None:
            return auth_dict
        return auth_dict.get("token", None)
