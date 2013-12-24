# -*- coding: utf-8 -*-

"""
gmncurses.ui.views.projects
---------~~~~~~~~~~~~~~~~~~
"""

import functools

import urwid

from gmncurses.ui import widgets

from . import base

from .backlog import ProjectBacklogSubView
from .milestones import ProjectMilestoneSubView
from .issues import ProjectIssuesSubView
from .wiki import ProjectWikiSubView


class ProjectsView(base.View):
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


class ProjectDetailView(base.View):
    TABS = ["Backlog", "Sprints", "Issues", "Wiki", "Admin"]

    def __init__(self, project):
        self.project = project

        self.notifier = widgets.FooterNotifier("")

        self.tabs = widgets.Tabs(self.TABS)

        # Subviews
        self.backlog = ProjectBacklogSubView(project, self.notifier, self.tabs)
        self.sprint = ProjectMilestoneSubView(project, self.notifier, self.tabs)
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
        self.widget.set_body(self.wiki.widget)

    def admin_view(self):
        self.tabs.tab_list.focus = 4
        self.widget.set_body(self.admin.widget)


class ProjectAdminSubView(base.SubView):
    def __init__(self, project, notifier, tabs):
        self.project = project
        self.notifier = notifier

        self.widget = urwid.ListBox(urwid.SimpleListWalker([
            tabs,
            widgets.box_solid_fill(" ", 1),
        ]))
