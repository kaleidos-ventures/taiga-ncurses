# -*- coding: utf-8 -*-

"""
taiga_ncurses.ui.views.projects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import functools

import urwid

from taiga_ncurses.ui.widgets import generic, projects

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
        grid = generic.Grid([], 4, 2, 2, 'center')
        fill = urwid.Filler(grid, min_height=40)
        self.notifier = generic.FooterNotifier("")
        self.widget = urwid.Frame(fill,
                                  header=generic.Header(),
                                  footer=generic.Footer(self.notifier))

    def populate(self, projects):
        self.projects = projects
        self.project_buttons = [urwid.Button(p['name']) for p in projects]
        min_width = functools.reduce(max, (len(p['name']) for p in projects), 0)
        grid = generic.Grid(self.project_buttons, min_width * 4, 2, 2, 'center')
        self.widget.set_body(urwid.Filler(grid, min_height=40))


class ProjectDetailView(base.View):
    TABS = ["Backlog", "Milestones", "Issues", "Wiki", "Admin"]

    def __init__(self, project):
        self.project = project

        self.notifier = generic.FooterNotifier("")

        self.tabs = generic.Tabs(self.TABS)

        # Subviews
        self.backlog = ProjectBacklogSubView(self, project, self.notifier, self.tabs)
        self.sprint = ProjectMilestoneSubView(self, project, self.notifier, self.tabs)
        self.issues = ProjectIssuesSubView(self, project, self.notifier, self.tabs)
        self.wiki = ProjectWikiSubView(self, project, self.notifier, self.tabs)
        self.admin = ProjectAdminSubView(self, project, self.notifier, self.tabs)

        self.widget = urwid.Frame(self.backlog.widget,
                                  header=projects.ProjectDetailHeader(project),
                                  footer=generic.Footer(self.notifier))

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
    def __init__(self, parent_view, project, notifier, tabs):
        super().__init__(parent_view)

        self.project = project
        self.notifier = notifier

        self.widget = urwid.ListBox(urwid.SimpleListWalker([
            tabs,
            generic.box_solid_fill(" ", 1),
        ]))
