# -*- coding: utf-8 -*-

"""
gmncurses.ui.views
~~~~~~~~~~~~~~~~~~
"""

import operator
import functools

import urwid

from . import widgets


class View(object):
    widget = None
    notifier = None


class LoginView(View):
    login_button = None

    def __init__(self, username_text, password_text):
        # Header
        header = widgets.banner()
        # Username and password prompts
        max_prompt_length = max(len(username_text), len(password_text))
        max_prompt_padding = max_prompt_length + 2

        self._username_editor = widgets.editor()
        username_prompt = widgets.username_prompt(username_text, self._username_editor, max_prompt_padding)
        self._password_editor = widgets.editor(mask="♥")
        password_prompt = widgets.password_prompt(password_text, self._password_editor, max_prompt_padding)
        # Login button
        self.login_button = widgets.button("login")
        login_button_widget = widgets.wrap_login_button(self.login_button)
        # Notifier
        self.notifier = widgets.Notifier("")

        login_widget = widgets.Login([header, username_prompt, password_prompt, login_button_widget, self.notifier])
        self.widget = widgets.center(login_widget)

    @property
    def username(self):
        return self._username_editor.get_edit_text()

    @property
    def password(self):
        return self._password_editor.get_edit_text()


class ProjectsView(View):
    project_buttons = None
    projects = None

    def __init__(self, projects):
        self.projects = projects
        self.project_buttons = [urwid.Button(p['name']) for p in projects]
        min_width = functools.reduce(max, (len(p['name']) for p in projects), 0)
        grid = widgets.Grid(self.project_buttons, min_width * 4, 2, 2, 'center')
        fill = urwid.Filler(grid, min_height=40)
        self.notifier = widgets.ProjectsNotifier("")
        self.widget = urwid.Frame(fill,
                                  header=widgets.ProjectsHeader(),
                                  footer=widgets.ProjectsFooter(self.notifier))


class ProjectDetailView(View):
    def __init__(self, project):
        self.project = project

        self.widget = urwid.Frame(urwid.SolidFill())

