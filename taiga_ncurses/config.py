# -*- coding: utf-8 -*-

"""
taiga_ncurses.config
~~~~~~~~~~~~~~~~
"""

import os
import urllib
from configobj import ConfigObj


DEFAULT_CONFIG_DIR =  os.path.join(os.environ["HOME"], ".taiga-ncurses")
DEFAULT_CONFIG_FILE = os.path.join(DEFAULT_CONFIG_DIR, "config.ini")

DEFAULT_PALETTE = {
    "default":                  ("white", "default"),
    "editor":                   ("white,underline", "black", ),
    "password-editor":          ("light red,underline", "black"),
    "submit-button":            ("white", "dark green"),
    "cancel-button":            ("black", "light gray"),
    "popup":                    ("white","dark gray"),
    "popup-section-title":      ("white,underline,bold", "dark gray"),
    "popup-editor":             ("white,underline", "dark gray"),
    "popup-submit-button":      ("white", "dark green"),
    "popup-cancel-button":      ("black", "light gray"),
    "popup-selected":           ("dark cyan", "black"),
    "popup-text-magenta":       ("light magenta", "dark gray"),
    "popup-text-red":           ("dark red", "dark gray"),
    "error":                    ("white", "dark red"),
    "info":                     ("white", "dark blue"),
    "green":                    ("dark green", "default"),
    "red":                      ("dark red", "default"),
    "yellow":                   ("yellow", "default"),
    "cyan":                     ("dark cyan", "default"),
    "magenta":                  ("light magenta", "default"),
    "green-bg":                 ("white", "dark green"),
    "projects-button":          ("black", "dark green"),
    "account-button":           ("black", "dark green"),
    "help-button":              ("white", "black"),
    "footer":                   ("black", "black"),
    "footer-error":             ("dark red", "black"),
    "footer-info":              ("light blue", "black"),
    "active-tab":               ("white", "dark blue"),
    "inactive-tab":             ("white", "default"),
    "focus":                    ("black", "dark cyan"),
    "focus-header":             ("black", "dark green"),
    "progressbar-normal":       ("black", "dark gray", "standout"),
    "progressbar-complete":     ("white", "dark green"),
    "progressbar-smooth":       ("dark green","dark gray"),
    "progressbar-normal-red":   ("black", "dark gray", "standout"),
    "progressbar-complete-red": ("white", "dark red"),
    "progressbar-smooth-red":   ("dark red","dark gray")
}


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
    "main": {
        "host": {
            "scheme": "http",
            "domain": "localhost",
            "port": "8000",
        },
        "site": {
            "domain": "localhost",
        },
        "palette": "default",
        "keys": Keys.config
    },
    "projects": {
        "keys": ProjectKeys.config
    },
    "backlog": {
        "keys": ProjectBacklogKeys.config
    },
    "milestone": {
        "keys": ProjectMilestoneKeys.config
    },
    "issues": {
        "keys": ProjectIssuesKeys.config
    },
    "palettes": {
        "default": DEFAULT_PALETTE
    }
}


class Configuration(object):
    def __init__(self,
                 config_dict=None,
                 config_file=DEFAULT_CONFIG_FILE):
        self.config_file = config_file

        self.config = ConfigObj(infile=DEFAULTS.copy(),
                                encoding="utf-8",
                                create_empty=True)
        self.config.update({} if config_dict is None else config_dict)
        self.config.filename = self.config_file

    def load(self):
        config = ConfigObj(infile=self.config_file,
                           encoding="utf-8")
        self.config.merge(config)

    def save(self):
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        self.config.write()

    @property
    def host(self):
        host = self.config["main"]["host"]

        scheme = host["scheme"]
        assert scheme in ("http", "https")
        domain = urllib.parse.quote(host["domain"])
        port = ":{}".format(host["port"]) if "port" in host else ""

        return "{scheme}://{domain}{port}".format(scheme=scheme,
                                                  domain=domain,
                                                  port=port)

    @property
    def site(self):
        site =  self.config["main"]["site"]
        domain = urllib.parse.quote(site["domain"])
        return domain

    @property
    def auth_token(self):
        return self.config.get("auth", {}).get("token", None)

    @auth_token.setter
    def auth_token(self, auth_token):
        self.config.merge({"auth": {"token": auth_token}})

    @property
    def palette(self):
        palette_name = self.config["main"].get("palette", "default")
        palette_dict = self.config["palettes"].get(palette_name, DEFAULT_PALETTE)
        return [(k,) + v for k, v in palette_dict.items()]
