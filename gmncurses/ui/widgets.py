# -*- coding: utf-8 -*-

"""
gmncurses.ui.widgets
~~~~~~~~~~~~~~~~~~~~
"""

import urwid

from . import mixins
from gmncurses import data


def box_solid_fill(char, height):
    sf = urwid.SolidFill(char)
    return urwid.BoxAdapter(sf, height=height)


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


class Grid(mixins.ViMotionMixin, mixins.EmacsMotionMixin, urwid.GridFlow):
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
    def __init__(self, project, project_stats):
        widget = urwid.Columns([
            ("weight", 0.3, urwid.Pile([TotalPoints(project_stats), TotalSprints(project)])),
            ("weight", 0.3, urwid.Pile([ClosedPoints(project_stats), CompletedSprints(project)])),
            ("weight", 0.3, urwid.Pile([DefinedPoints(project_stats), CurrentSprint(project)])),
        ])
        super().__init__(widget)


class TotalPoints(urwid.Text):
    def __init__(self, project_stats):
        text = ["Total points: ", ("cyan", str(data.total_points(project_stats)))]
        super().__init__(text)


class TotalSprints(urwid.Text):
    def __init__(self, project):
        text = ["Total sprints: ", ("cyan", str(data.total_sprints(project)))]
        super().__init__(text)


class ClosedPoints(urwid.Text):
    def __init__(self, project_stats):
        text = [
            "Closed points: ",
            ("green", str(data.closed_points(project_stats))),
            " (",
            ("green", "{0:.1f} %".format(data.closed_points_percentage(project_stats))),
            ")",
        ]
        super().__init__(text)


class DefinedPoints(urwid.Text):
    def __init__(self, project_stats):
        text = [
            "Defined points: ",
            ("red", str(data.defined_points(project_stats))),
            " (",
            ("red", "{0:.1f} %".format(data.defined_points_percentage(project_stats))),
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


class UserStoryList(mixins.ViMotionMixin,
                    mixins.EmacsMotionMixin,
                    urwid.WidgetWrap):
    def __init__(self):
        columns = urwid.Columns([
            ("weight", 0.6, ListCell("US")),
            ("weight", 0.1, ListCell("UX")),
            ("weight", 0.1, ListCell("Design")),
            ("weight", 0.1, ListCell("Front")),
            ("weight", 0.1, ListCell("Back")),
        ])
        self.widget = urwid.ListBox(urwid.SimpleFocusListWalker([columns]))
        super().__init__(urwid.BoxAdapter(self.widget, height=30))

    def populate(self, user_stories):
        first_gains_focus = len(self.widget.body) == 1 and user_stories

        for us in user_stories:
            self.widget.body.append(UserStoryEntry(us))

        if first_gains_focus:
            self.widget.set_focus(1)


class UserStoryEntry(urwid.WidgetWrap):
    def __init__(self, us):
        us_id_and_name = "#{0: <10} {1}".format(str(data.us_id(us)), data.us_subject(us))
        us_name = ListText(us_id_and_name, align="left")
        ux_points = ListText(str(data.us_ux_points(us)))
        design_points = ListText(str(data.us_design_points(us)))
        front_points = ListText(str(data.us_front_points(us)))
        back_points = ListText(str(data.us_back_points(us)))
        self.widget = urwid.Columns([
            ("weight", 0.6, us_name),
            ("weight", 0.1, ux_points),
            ("weight", 0.1, design_points),
            ("weight", 0.1, front_points),
            ("weight", 0.1, back_points),
        ])
        super().__init__(urwid.AttrMap(self.widget, "default", "focus"))

    def selectable(self):
        return True


class ListCell(urwid.WidgetWrap):
    def __init__(self, text):
        text_widget = urwid.AttrMap(ListText(text), "default")
        widget = urwid.AttrMap(urwid.LineBox(text_widget), "green")
        super().__init__(widget)


class ListText(mixins.IgnoreKeyPressMixin, urwid.Text):
    def __init__(self, text, align="center"):
        super().__init__(text, align=align)

