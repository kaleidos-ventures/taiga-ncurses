# -*- coding: utf-8 -*-

"""
taiga_ncurses.config
~~~~~~~~~~~~~~~~~~~~
"""

import os
import urllib


###########################################################
# Default config settings
###########################################################

DEFAULT_CONFIG_DIR =  os.path.join(os.environ["HOME"], ".taiga-ncurses")
DEFAULT_CONFIG_FILE = os.path.join(DEFAULT_CONFIG_DIR, "config.ini")

# Default color palette

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

# Default keyboard shortcut

MAIN_KEYS = {
    "quit": "q",
    "debug": "D",
    "projects": "P",
    "backlog": "B",
    "milestone": "M",
    "issues": "I",
    "wiki": "W",
    "admin": "A"
}

BACKLOG_KEYS = {
    "create": "n",
    "create_in_bulk": "N",
    "edit": "e",
    "delete": "delete",
    "update_order": "w",
    "move_to_milestone": "m",
    "increase_priority": "K",
    "decrease_priority": "J",
    "reload": "r",
    "help":"?"
}

MILESTONE_KEYS = {
    "create_user_story": "N",
    "create_task": "n",
    "edit": "e",
    "delete": "delete",
    "change_to_milestone": "m",
    "reload": "r",
    "help": "?"
}

ISSUES_KEYS = {
    "create": "n",
    "edit": "e",
    "delete": "delete",
    "filters": "f",
    "reload": "r",
    "help": "?"
}

# Default settings

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
        "keys": MAIN_KEYS
    },
    "backlog": {
        "keys": BACKLOG_KEYS
    },
    "milestone": {
        "keys": MILESTONE_KEYS
    },
    "issues": {
        "keys": ISSUES_KEYS
    },
    "palettes": {
        "default": DEFAULT_PALETTE
    },
    "auth": {
        "token": None,
    }
}

class ConfigData:
    def __init__(self, data):
        super().__setattr__('_data', data)

    def __dir__(self):
        return self._data.keys()

    def __getattr__(self, name):
        if name not in self._data:
            raise AttributeError

        if isinstance(self._data[name], dict):
            return self.__class__(self._data[name])

        return self._data[name]

    def __setattr__(self, name, value):
        self._data[name] = value

    def __delattr__(self, name):
        if name not in self._data:
            raise AttributeError

        del self._data[name]

    def items(self):
        return self._data.items()


class ConfiguratioManager:
    def __init__(self, config_file=DEFAULT_CONFIG_FILE):
        self.config_file = config_file
        self.data = ConfigData(DEFAULTS.copy())

    def load(self):
        # TODO
        pass

    def save(self):
        # TODO
        pass

    @property
    def host(self) -> str:
        scheme = self.data.main.host.scheme
        assert scheme in ("http", "https")
        domain = urllib.parse.quote(self.data.main.host.domain)
        try:
            port = ":{}".format(self.data.main.host.port)
        except AttributeError:
            port = ""
        return "{scheme}://{domain}{port}".format(scheme=scheme,
                                                  domain=domain,
                                                  port=port)

    @property
    def palette(self):
        palette_name = self.data.main.palette
        try:
            palette_dict = getattr(self.data.palettes, palette_name)
        except AttributeError:
            palette_dict = DEFAULT_PALETTE
        return [(k,) + tuple(v) for k, v in palette_dict.items()]


settings = ConfiguratioManager()
