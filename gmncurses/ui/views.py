# -*- coding: utf-8 -*-

"""
gmncurses.ui.views
~~~~~~~~~~~~~~~~~~
"""

import functools

import urwid

from . import widgets


class View(object):
    widget = None
    notifier = None


class SubView(object):
    widget = None


# Auth

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

        login_widget = widgets.Login([header, username_prompt, password_prompt, login_button_widget,
                                      self.notifier])
        self.widget = widgets.center(login_widget)

    @property
    def username(self):
        return self._username_editor.get_edit_text()

    @property
    def password(self):
        return self._password_editor.get_edit_text()


# Projects List

class ProjectsView(View):
    project_buttons = None
    projects = None

    def __init__(self):
        self.projects = []
        self.project_buttons = []
        grid = widgets.Grid([], 4, 2, 2, 'center')
        fill = urwid.Filler(grid, min_height=40)
        self.notifier = widgets.FooterNotifier("")
        self.widget = urwid.Frame(fill,
                                  header=widgets.ProjectsHeader(),
                                  footer=widgets.Footer(self.notifier))

    def populate(self, projects):
        self.projects = projects
        self.project_buttons = [urwid.Button(p['name']) for p in projects]
        min_width = functools.reduce(max, (len(p['name']) for p in projects), 0)
        grid = widgets.Grid(self.project_buttons, min_width * 4, 2, 2, 'center')
        self.widget.set_body(urwid.Filler(grid, min_height=40))


# Project Detail

class ProjectDetailView(View):
    TABS = ["Backlog", "Sprints", "Issues", "Wiki", "Admin"]

    def __init__(self, project):
        self.project = project

        self.notifier = widgets.FooterNotifier("")

        self.tabs = widgets.Tabs(self.TABS)

        # Subviews
        self.backlog = ProjectBacklogSubView(project, self.notifier, self.tabs)
        self.sprint = ProjectSprintSubView(project, self.notifier, self.tabs)
        self.issues = ProjectIssuesSubView(project, self.notifier, self.tabs)
        self.wiki = ProjectWikiSubView(project, self.notifier, self.tabs)
        self.admin = ProjectAdminSubView(project, self.notifier, self.tabs)

        self.widget = urwid.Frame(self.backlog.widget,
                                  header=widgets.ProjectDetailHeader(project),
                                  footer=widgets.Footer(self.notifier))

    def backlog_view(self):
        self.tabs.tab_list.focus = 0
        self.widget.set_body(self.backlog.widget)

    def sprint_view(self):
        self.tabs.tab_list.focus = 1
        self.widget.set_body(self.sprint.widget)

    def issues_view(self):
        self.tabs.tab_list.focus = 2
        self.widget.set_body(self.issues.widget)

    def wiki_view(self):
        self.tabs.tab_list.focus = 3
        self.widget.set_body(self.issues.widget)

    def admin_view(self):
        self.tabs.tab_list.focus = 4
        self.widget.set_body(self.issues.widget)


class ProjectBacklogSubView(SubView):
    def __init__(self, project, notifier, tabs):
        self.project = project
        self.notifier = notifier

        self.stats = widgets.ProjectBacklogStats(project)
        self.user_stories = widgets.UserStoryList(project)

        list_walker = urwid.SimpleFocusListWalker([
            tabs,
            widgets.box_solid_fill(" ", 1),
            self.stats,
            widgets.box_solid_fill(" ", 1),
            self.user_stories
        ])
        list_walker.set_focus(4)
        self.widget = urwid.ListBox(list_walker)


class ProjectSprintSubView(SubView):
    def __init__(self, project, notifier, tabs):
        self.project = project
        self.notifier = notifier

        self.widget = urwid.ListBox(urwid.SimpleListWalker([
            tabs,
            widgets.box_solid_fill(" ", 1),
        ]))


class ProjectIssuesSubView(SubView):
    def __init__(self, project, notifier, tabs):
        self.project = project
        self.notifier = notifier

        self.stats = widgets.ProjectIssuesStats(project)
        self.issues = widgets.IssuesList(project)

        list_walker = urwid.SimpleFocusListWalker([
            tabs,
            widgets.box_solid_fill(" ", 1),
            self.stats,
            widgets.box_solid_fill(" ", 1),
            self.issues
        ])
        list_walker.set_focus(4)
        self.widget = urwid.ListBox(list_walker)


class ProjectWikiSubView(SubView):
    def __init__(self, project, notifier, tabs):
        self.project = project
        self.notifier = notifier

        self.widget = urwid.ListBox(urwid.SimpleListWalker([
            tabs,
            widgets.box_solid_fill(" ", 1),
        ]))


class ProjectAdminSubView(SubView):
    def __init__(self, project, notifier, tabs):
        self.project = project
        self.notifier = notifier

        self.widget = urwid.ListBox(urwid.SimpleListWalker([
            tabs,
            widgets.box_solid_fill(" ", 1),
        ]))
