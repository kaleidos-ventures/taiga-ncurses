# -*- coding: utf-8 -*-

"""
gmncurses.ui.widgets
~~~~~~~~~~~~~~~~~~~~
"""

import urwid

from . import mixins
from gmncurses import data

def wrap_in_whitespace(widget, cls=urwid.Columns):
    whitespace = urwid.SolidFill(" ")
    return cls([whitespace, widget, whitespace])


def center(widget):
    return wrap_in_whitespace(wrap_in_whitespace(widget), cls=urwid.Pile)


def banner():
    bt = urwid.BigText("GreenMine", font=urwid.font.HalfBlock7x7Font())
    btwp = urwid.Padding(bt, "center", width="clip")
    return urwid.AttrWrap(btwp, "green")


def username_prompt(username_text, editor, max_prompt_padding):
    username = urwid.Text(username_text, "center")
    return urwid.Columns([(len(username_text), username),
                          (max_prompt_padding - len(username_text), urwid.Text("")),
                          urwid.AttrWrap(editor, "editor")])


def password_prompt(password_text, editor, max_prompt_padding):
    password = urwid.Text(password_text, "center")
    return urwid.Columns([(len(password_text), password),
                          (max_prompt_padding - len(password_text), urwid.Text("")),
                          urwid.AttrWrap(editor, "password-editor")])


def wrap_login_button(button):
    return urwid.AttrWrap(urwid.LineBox(button), "save-button")


def button(text, align=None):
    return PlainButton(text.upper(), align)


def editor(mask=None):
    if mask is None:
        return urwid.Edit()
    else:
        return urwid.Edit(mask=mask)


class Login(mixins.FormMixin, urwid.ListBox):
    def __init__(self, widgets):
        super(Login, self).__init__(urwid.SimpleListWalker(widgets))


class Notifier(mixins.NotifierMixin, urwid.Text):
    pass


class PlainButton(mixins.PlainButtonMixin, urwid.Button):
    ALIGN = "center"

    def __init__(self, text, align=None):
        super().__init__(text)
        self._label.set_align_mode(self.ALIGN if align is None else align)


class ProjectsHeader(urwid.WidgetWrap):
    def __init__(self):
        text = urwid.Text("GREENMINE")
        self.account_button = PlainButton("My account")
        cols = urwid.Columns([
            ("weight", 0.9, text),
            ("weight", 0.1, urwid.AttrMap(self.account_button, "account-button")),
        ])
        super().__init__(urwid.AttrMap(cols, "green-bg"))


class FooterNotifier(Notifier):
    ALIGN = "left"
    ERROR_PREFIX = "[ERROR]: "
    ERROR_ATTR = "footer-error"
    INFO_PREFIX = "[INFO]: "
    INFO_ATTR = "footer-info"


class Footer(urwid.WidgetWrap):
    def __init__(self, notifier):
        assert isinstance(notifier, FooterNotifier)
        cols = urwid.Columns([
            ("weight", 0.9, urwid.AttrMap(notifier, "footer")),
            ("weight", 0.1, urwid.AttrMap(PlainButton("? Help"), "help-button")),
        ])
        super().__init__(cols)


class ProjectDetailHeader(urwid.WidgetWrap):
    def __init__(self, project):
        text = urwid.Text("GREENMINE")
        self.title = urwid.Text(project["name"], align="left")
        self.projects_button = PlainButton("My projects")
        self.account_button = PlainButton("My account")
        cols = urwid.Columns([
            ("weight", 0.1, text),
            ("weight", 0.7, self.title),
            ("weight", 0.1, urwid.AttrMap(self.projects_button, "projects-button")),
            ("weight", 0.1, urwid.AttrMap(self.account_button, "account-button")),
        ])
        super().__init__(urwid.AttrMap(cols, "green-bg"))


class Grid(mixins.ViMotionMixin, urwid.GridFlow):
    pass


class Tabs(urwid.WidgetWrap):
    def __init__(self, tabs):
        self.tabs = urwid.MonitoredFocusList(tabs)
        texts = self._create_texts()
        super().__init__(urwid.Columns(texts))

    def _create_texts(self):
        texts = []
        for i, tab in enumerate(self.tabs):
            if i == self.tabs.focus:
                texts.append(urwid.AttrMap(urwid.LineBox(urwid.Text(tab + " ")), "active-tab"))
            else:
                texts.append(urwid.AttrMap(urwid.LineBox(urwid.Text(tab + " ")), "inactive-tab"))
        return texts

class ProjectBacklogStats(urwid.WidgetWrap):
    def __init__(self, project):
        widget = urwid.Columns([
            ("weight", 0.3, urwid.Pile([TotalPoints(project), TotalSprints(project)])),
            ("weight", 0.3, urwid.Pile([CompletedPoints(project), CompletedSprints(project)])),
            ("weight", 0.3, urwid.Pile([UnasignedPoints(project), CurrentSprint(project)])),
        ])
        super().__init__(widget)


class TotalPoints(urwid.Text):
    def __init__(self, project):
        text = ["Total points: ", ("green", str(data.total_points(project)))]
        super().__init__(text)


class TotalSprints(urwid.Text):
    def __init__(self, project):
        text = ["Total sprints: ", ("green", str(data.total_sprints(project)))]
        super().__init__(text)


class CompletedPoints(urwid.Text):
    def __init__(self, project):
        text = [
            "Completed points: ",
            ("red", str(data.completed_points(project))),
            " (",
            ("red", str(data.completed_points_percentage(project))),
            ")",
        ]
        super().__init__(text)


class UnasignedPoints(urwid.Text):
    def __init__(self, project):
        text = [
            "Unasigned points: ",
            ("red", str(data.unasigned_points(project))),
            " (",
            ("red", str(data.unasigned_points_percentage(project))),
            ")",
        ]
        super().__init__(text)


class CurrentSprint(urwid.Text):
    def __init__(self, project):
        text = [
            "Current sprint: ",
            ("cyan", str(data.current_sprint(project))),
            " (",
            ("cyan", str(data.current_sprint_name(project))),
            ")",
        ]
        super().__init__(text)


class CompletedSprints(urwid.Text):
    def __init__(self, project):
        text = ["Completed sprints: ", ("red", str(data.completed_sprints(project)))]
        super().__init__(text)


class UserStories(urwid.WidgetWrap):
    def __init__(self, user_stories):
        super().__init__(urwid.Text("USS"))
