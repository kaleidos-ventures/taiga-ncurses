# -*- coding: utf-8 -*-

"""
taiga_ncurses.config
~~~~~~~~~~~~~~~~
"""

import os
import urllib
from configparser import ConfigParser
from collections import ChainMap


DEFAULT_CONFIG_DIR =  os.path.join(os.environ["HOME"], ".taiga-ncurses")
DEFAULT_CONFIG_FILE = os.path.join(DEFAULT_CONFIG_DIR, "config.ini")
DEFAULT_AUTH_FILE = os.path.join(DEFAULT_CONFIG_DIR, "auth.ini")

PALETTE = [
    ("default", "white", "default"),
    ("editor", "white,underline", "black", ),
    ("password-editor", "light red,underline", "black"),
    ("submit-button", "white", "dark green"),
    ("cancel-button", "black", "light gray"),
    ("popup", "white", "dark gray"),
    ("popup-section-title", "white,underline,bold", "dark gray"),
    ("popup-editor", "white,underline", "dark gray"),
    ("popup-submit-button", "white", "dark green"),
    ("popup-cancel-button", "black", "light gray"),
    ("popup-selected", "dark cyan", "black"),
    ("popup-text-magenta", "light magenta", "dark gray"),
    ("popup-text-red", "dark red", "dark gray"),
    ("error", "white", "dark red"),
    ("info", "white", "dark blue"),
    ("green", "dark green", "default"),
    ("red", "dark red", "default"),
    ("yellow", "yellow", "default"),
    ("cyan", "dark cyan", "default"),
    ("magenta", "light magenta", "default"),
    ("green-bg", "white", "dark green"),
    ("projects-button", "black", "dark green"),
    ("account-button", "black", "dark green"),
    ("help-button", "white", "black"),
    ("footer", "black", "black"),
    ("footer-error", "dark red", "black"),
    ("footer-info", "light blue", "black"),
    ("active-tab", "white", "dark blue"),
    ("inactive-tab", "white", "default"),
    ("focus", "black", "dark cyan"),
    ("focus-header", "black", "dark green"),
    ('progressbar-normal', 'black', 'dark gray', 'standout'),
    ('progressbar-complete', 'white', 'dark green'),
    ('progressbar-smooth', 'dark green','dark gray'),
    ('progressbar-normal-red', 'black', 'dark gray', 'standout'),
    ('progressbar-complete-red', 'white', 'dark red'),
    ('progressbar-smooth-red', 'dark red','dark gray')
]


class KeyConfigMeta(type):
    def __new__(cls, clsname, bases, dct):
        dct["config"] = {v: k.capitalize().replace("_", " ") for k, v in dct.items() if k.isupper()}
        return super().__new__(cls, clsname, bases, dct)


class Keys(metaclass=KeyConfigMeta):
    QUIT = "q"
    DEBUG = "D"


class ProjectKeys(metaclass=KeyConfigMeta):
    PROJECTS = "P"
    BACKLOG = "B"
    MILESTONES = "M"
    ISSUES = "I"
    WIKI = "W"
    ADMIN = "A"


class ProjectBacklogKeys(metaclass=KeyConfigMeta):
    CREATE_USER_STORY = "n"
    CREATE_USER_STORIES_IN_BULK = "N"
    EDIT_USER_STORY = "e"
    DELETE_USER_STORY = "delete"
    UPDATE_USER_STORIES_ORDER = "w"
    MOVE_US_TO_MILESTONE = "m"
    US_UP = "K"
    US_DOWN = "J"
    RELOAD = "r"
    HELP = "?"


class ProjectMilestoneKeys(metaclass=KeyConfigMeta):
    CREATE_USER_STORY = "N"
    CREATE_TASK = "n"
    EDIT_USER_STORY_OR_TASK = "e"
    DELETE_USER_STORY_OR_TASK = "delete"
    CHANGE_TO_MILESTONE = "m"
    RELOAD = "r"
    HELP = "?"


class ProjectIssuesKeys(metaclass=KeyConfigMeta):
    CREATE_ISSUE = "n"
    EDIT_ISSUE = "e"
    DELETE_ISSUE = "delete"
    FILTERS = "f"
    RELOAD = "r"
    HELP = "?"


DEFAULTS = {
    "keys": ChainMap(Keys.config,
                     ProjectKeys.config,
                     ProjectBacklogKeys.config,
                     ProjectMilestoneKeys.config,
                     ProjectIssuesKeys.config),
    "host": {
        "scheme": "http",
        "domain": "localhost",
        "port": "8000",
    },
    "site": {
        "domain": "localhost",
    }
}


class Configuration(object):
    def __init__(self,
                 config_dict=None,
                 config_file=DEFAULT_CONFIG_FILE,
                 auth_config_file=DEFAULT_AUTH_FILE,
                 config_dir=DEFAULT_CONFIG_DIR):
        self.config_dict = DEFAULTS.copy()
        self.config_dict.update({} if config_dict is None else config_dict)
        self.config_file = config_file
        self.auth_config_file = auth_config_file
        self.config_dir = config_dir

    def load(self):
        parser = ConfigParser()
        parser.read(self.config_file, encoding="utf-8")
        self.config_dict.update(parser._sections)
        auth_parser = ConfigParser()
        auth_parser.read(self.auth_config_file, encoding="utf-8")
        self.config_dict.update(auth_parser._sections)

    def save(self):
        try:
            os.mkdir(self.config_dir)
        except FileExistsError:
            pass
        self._save_config()
        self._save_auth()

    def _save_config(self):
        parser = ConfigParser()
        config_sections = (s for s in self.config_dict if s != "auth")
        for s in config_sections:
            parser.add_section(s)
            for k, v in self.config_dict[s].items():
                parser.set(s, k, str(v))
        with open(self.config_file, mode="w+", encoding="utf-8") as config_file:
            parser.write(config_file)

    def _save_auth(self):
        if "auth" in self.config_dict:
            parser = ConfigParser()
            parser.add_section("auth")
            parser.set("auth", "token", self.config_dict["auth"]["token"])
            with open(self.auth_config_file, mode="w+", encoding="utf-8") as auth_config_file:
                parser.write(auth_config_file)

    @property
    def host(self):
        host = self.config_dict["host"]

        scheme = host["scheme"]
        assert scheme in ("http", "https")
        domain = urllib.parse.quote(host["domain"])
        port = ":{}".format(host["port"]) if "port" in host else ""

        return "{scheme}://{domain}{port}".format(scheme=scheme, domain=domain, port=port)

    @property
    def site(self):
        site =  self.config_dict["site"]
        domain = urllib.parse.quote(site["domain"])
        return domain

    @property
    def auth_token(self):
        auth_dict = self.config_dict.get("auth", None)
        if auth_dict is None:
            return auth_dict
        return auth_dict.get("token", None)
