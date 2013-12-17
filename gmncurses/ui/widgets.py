# -*- coding: utf-8 -*-

"""
gmncurses.ui.widgets
~~~~~~~~~~~~~~~~~~~~
"""

import urwid
from x256 import x256

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


class Notifier(mixins.NotifierMixin, mixins.NonSelectableMixin, urwid.Text):
    pass


class PlainButton(mixins.PlainButtonMixin, urwid.Button):
    ALIGN = "center"

    def __init__(self, text, align=None):
        super().__init__(text)
        self._label.set_align_mode(self.ALIGN if align is None else align)


class ProjectsHeader(mixins.NonSelectableMixin, urwid.WidgetWrap):
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


class Footer(mixins.NonSelectableMixin, urwid.WidgetWrap):
    def __init__(self, notifier):
        assert isinstance(notifier, FooterNotifier)
        cols = urwid.Columns([
            ("weight", 0.9, urwid.AttrMap(notifier, "footer")),
            ("weight", 0.1, urwid.AttrMap(PlainButton("? Help"), "help-button")),
        ])
        super().__init__(cols)


class ProjectDetailHeader(mixins.NonSelectableMixin, urwid.WidgetWrap):
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


class Tabs(mixins.NonSelectableMixin, urwid.WidgetWrap):
    def __init__(self, tabs, focus=0):
        self.tab_list = urwid.MonitoredFocusList(tabs)
        self.tab_list.focus = focus
        self.tab_list.set_focus_changed_callback(self.rebuild_tabs)

        cols = [urwid.AttrMap(self.tab(t), "active-tab" if i == self.tab_list.focus else "inactive-tab")
                                for i, t in enumerate(tabs)]
        self.columns = urwid.Columns(cols)

        super().__init__(self.columns)

    def rebuild_tabs(self, new_focus):
        for i, c in enumerate(self.columns.contents):
            widget, _ = c
            widget.set_attr_map({None: "active-tab" if i == new_focus  else "inactive-tab"})

    def tab(self, text):
        return urwid.LineBox(urwid.Text(text + " "))


class ProjectBacklogStats(urwid.WidgetWrap):
    def __init__(self, project):
        self.project = project
        widget = urwid.Columns([
            ("weight", 0.3, urwid.Pile([urwid.Text("")])),
            ("weight", 0.3, urwid.Pile([urwid.Text("")])),
            ("weight", 0.3, urwid.Pile([urwid.Text("")])),
        ])
        super().__init__(widget)

    def populate(self, project_stats):
        self._w = urwid.Columns([
            ("weight", 0.3, urwid.Pile([TotalPoints(project_stats), TotalSprints(self.project)])),
            ("weight", 0.3, urwid.Pile([ClosedPoints(project_stats), CompletedSprints(self.project)])),
            ("weight", 0.3, urwid.Pile([DefinedPoints(project_stats), CurrentSprint(self.project)])),
        ])


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
        text = ["Completed sprints: ", ("green", str(len(data.completed_sprints(project))))]
        super().__init__(text)


class UserStoryList(mixins.ViMotionMixin, mixins.EmacsMotionMixin, urwid.WidgetWrap):
    def __init__(self, project):
        self.project = project
        self.roles = data.computable_roles(project)

        colum_items = [("weight", 0.6, ListCell("US"))]
        colum_items.append(("weight", 0.08, ListCell("Status")))
        colum_items.extend([("weight", 0.05, ListCell(r["name"])) for r in self.roles])
        colum_items.append(("weight", 0.05, ListCell(("green", "TOTAL"))))
        colum_items.append(("weight", 0.05, ListCell(("cyan", "SUM."))))

        columns = urwid.Columns(colum_items)
        self.widget = urwid.Pile([columns])
        super().__init__(self.widget)

    def populate(self, user_stories, project_stats):
        if user_stories:
            self.reset()

        self.doomline_limit = data.doomline_limit_points(project_stats)
        first_gains_focus = len(self.widget.contents) == 1 and user_stories

        summation = 0
        doomline = False

        for us in user_stories:
            summation += data.us_total_points(us)

            if not doomline and summation > self.doomline_limit:
                self.widget.contents.append((RowDivider("red"), ("weight", 0.1)))
                doomline = True

            self.widget.contents.append((UserStoryEntry(us, self.project, self.roles, summation),
                                         ("weight", 0.1)))

        if first_gains_focus:
            t = self.widget.contents
            self.widget.contents.focus = 1

    def reset(self):
        self.widget.contents = self.widget.contents[:1]


class UserStoryEntry(urwid.WidgetWrap):
    def __init__(self, us, project, roles, summation=0.0):
        us_ref_and_name = "#{0: <6} {1}".format(str(data.us_ref(us)), data.us_subject(us))
        colum_items = [("weight", 0.6, ListText(us_ref_and_name, align="left"))]

        hex_color, status = data.us_status_with_color(us, project)
        color = x256.from_hex(color_to_hex(hex_color))
        attr = urwid.AttrSpec("h{0}".format(color), "default")
        colum_items.append(("weight", 0.08, ListText( (attr, status) )))

        points_by_role = data.us_points_by_role(us, project, roles)
        for point in points_by_role:
            colum_items.append(("weight", 0.05, ListText(str(point))))
        colum_items.append(("weight", 0.05, ListText(("green", "{0:.1f}".format(data.us_total_points(us))))))
        colum_items.append(("weight", 0.05, ListText(("cyan", "{0:.1f}".format(summation)))))

        self.widget = urwid.Columns(colum_items)
        super().__init__(urwid.AttrMap(self.widget, "default", "focus"))

    def selectable(self):
        return True


# Issues

class ProjectIssuesStats(urwid.WidgetWrap):
    def __init__(self, project):
        self.project = project
        widget = urwid.Columns([
            ("weight", 0.25, urwid.Pile([urwid.Text("")])),
            ("weight", 0.25, urwid.Pile([urwid.Text("")])),
            ("weight", 0.25, urwid.Pile([urwid.Text("")])),
            ("weight", 0.25, urwid.Pile([urwid.Text("")])),
        ])
        super().__init__(widget)

    def populate(self, issues_stats):
        issues_statuses_stats = [urwid.Text(("cyan", "Per Status")),]
        issues_statuses_stats += [IssuesStatusStat(**ists) for ists in
                                  data.issues_statuses_stats(issues_stats).values()]
        issues_priorities_stats = [urwid.Text(("cyan", "Per Priority")),]
        issues_priorities_stats += [IssuesPriorityStat(**iprs) for iprs in
                                    data.issues_priorities_stats(issues_stats).values()]
        issues_severities_stats = [urwid.Text(("cyan", "Per Severity")),]
        issues_severities_stats += [IssuesSeverityStat(**ises) for ises in
                                    data.issues_severities_stats(issues_stats).values()]

        self._w = urwid.Columns([
            ("weight", 0.25, urwid.Pile([urwid.Text(""),
                TotalIssues(issues_stats), OpenedIssues(issues_stats), ClosedIssues(issues_stats)])),
            ("weight", 0.25, urwid.Pile(issues_statuses_stats)),
            ("weight", 0.25, urwid.Pile(issues_priorities_stats)),
            ("weight", 0.25, urwid.Pile(issues_severities_stats)),
        ])


class TotalIssues(urwid.Text):
    def __init__(self, issues_stats):
        text = ["Total issues: ", ("cyan", str(data.total_issues(issues_stats)))]
        super().__init__(text)


class OpenedIssues(urwid.Text):
    def __init__(self, issues_stats):
        text = ["Opened issues: ", ("red", str(data.opened_issues(issues_stats)))]
        super().__init__(text)


class ClosedIssues(urwid.Text):
    def __init__(self, issues_stats):
        text = ["Closed issues: ", ("green", str(data.closed_issues(issues_stats)))]
        super().__init__(text)


class IssuesStatusStat(urwid.Text):
    def __init__(self, name="", color="", count="", **kwargs):
        text = ["{}: ".format(name), (color, str(count))]
        super().__init__(text)


class IssuesPriorityStat(urwid.Text):
    def __init__(self, name="", color="", count="", **kwargs):
        text = ["{}: ".format(name), (color, str(count))]
        super().__init__(text)


class IssuesSeverityStat(urwid.Text):
    def __init__(self, name="", color="", count="", **kwargs):
        text = ["{}: ".format(name), (color, str(count))]
        super().__init__(text)


class IssuesList(mixins.ViMotionMixin, mixins.EmacsMotionMixin, urwid.WidgetWrap):
    def __init__(self, project):
        self.project = project

        colum_items = [("weight", 0.55, ListCell("Issue"))]
        colum_items.append(("weight", 0.1, ListCell("Status")))
        colum_items.append(("weight", 0.1, ListCell("Priority")))
        colum_items.append(("weight", 0.1, ListCell("Severity")))
        colum_items.append(("weight", 0.15, ListCell("Assigned to")))

        columns = urwid.Columns(colum_items)
        self.widget = urwid.Pile([columns])
        super().__init__(self.widget)

    def populate(self, issues):
        if issues:
            self.reset()

        first_gains_focus = len(self.widget.contents) == 1 and issues

        for issue in issues:
            self.widget.contents.append((IssueEntry(issue, self.project),
                                         ("weight", 0.1)))

        if first_gains_focus:
            t = self.widget.contents
            self.widget.contents.focus = 1

    def reset(self):
        self.widget.contents = self.widget.contents[:1]


class IssueEntry(urwid.WidgetWrap):
    def __init__(self, issue, project):
        issue_ref_and_name = "#{0: <4} {1}".format(str(data.issue_ref(issue)), data.issue_subject(issue))

        colum_items = [("weight", 0.55, ListText(issue_ref_and_name, align="left"))]

        hex_color, status = data.issue_status_with_color(issue, project)
        color = x256.from_hex(color_to_hex(hex_color))
        attr = urwid.AttrSpec("h{0}".format(color), "default")
        colum_items.append(("weight", 0.1, ListText((attr, status))))

        hex_color, priority = data.issue_priority_with_color(issue, project)
        color = x256.from_hex(color_to_hex(hex_color))
        attr = urwid.AttrSpec("h{0}".format(color), "default")
        colum_items.append(("weight", 0.1, ListText((attr, priority))))

        hex_color, severity = data.issue_severity_with_color(issue, project)
        color = x256.from_hex(color_to_hex(hex_color))
        attr = urwid.AttrSpec("h{0}".format(color), "default")
        colum_items.append(("weight", 0.1, ListText((attr, severity))))

        hex_color, username =  data.issue_assigned_to_with_color(issue, project)
        color = x256.from_hex(color_to_hex(hex_color))
        attr = urwid.AttrSpec("h{0}".format(color), "default")
        colum_items.append(("weight", 0.15, ListText((attr, username))))

        self.widget = urwid.Columns(colum_items)
        super().__init__(urwid.AttrMap(self.widget, "default", "focus"))

    def selectable(self):
        return True



# Sprints

class ProjectSprintsStats(urwid.WidgetWrap):
    def __init__(self, project):
        self.project = project
        widget = urwid.Columns([
                                ("weight", 0.25, urwid.Pile([urwid.Text("testing")])),
                                ("weight", 0.25, urwid.Pile([urwid.Text("testing")])),
                                ("weight", 0.20, urwid.Pile([urwid.Text("testing")])),
                                ("weight", 0.30, urwid.Pile([urwid.Text("testing")])),
                                ])
        super().__init__(widget)

    def populate(self, milestone_stats):
        completed_points = sum(milestone_stats["completed_points"])
        total_points = sum(milestone_stats["total_points"].values())
        rem_points = total_points - completed_points
        completed_tasks = milestone_stats["completed_tasks"]
        total_tasks = milestone_stats["total_tasks"]
        rem_tasks = total_tasks - completed_tasks
        #div_down = (total_points - completed_points)
        #if div_down == 0:
            #div_down = 1
        #percent_points_completed = total_points / div_down - 100
        percent_points_completed = '{0:.3}'.format(completed_points * 100 / total_points)
        self._w = urwid.Columns([
                                 ("weight", 0.20, urwid.Pile([urwid.Text("Completed points"), Color_text("cyan", str(percent_points_completed) + " %")])),
                                 ("weight", 0.30, urwid.Pile([urwid.Text("---")])),
                                 ("weight", 0.30, urwid.Pile([urwid.Text("---")])),
                                 ("weight", 0.20, urwid.Pile([urwid.Text("---")])),
                                 ])

class Color_text(urwid.Text):
    def __init__(self, color, text):
        text = [(color, text)]
        super().__init__(text)


# Wiki

class WikiPage(urwid.WidgetWrap):
    def __init__(self, project):
        self.project = project

        self.widget = urwid.Pile([ListText("No page found")])
        super().__init__(self.widget)

    def populate(self, wiki_page):
        slug_widget = ListText(data.slug(wiki_page))
        content_widget = urwid.Edit(edit_text=data.content(wiki_page), multiline=True, wrap='any',
                                     allow_tab=True)
        self.widget.contents = [
            (slug_widget, ('weight', 1)),
            (RowDivider(div_char=" "), ("weight", 0.1)),
            (content_widget, ('pack', None))
        ]
        self.widget.contents.focus = 2

# Misc

class ListCell(urwid.WidgetWrap):
    def __init__(self, text):
        text_widget = urwid.AttrMap(ListText(text), "default")
        widget = urwid.AttrMap(urwid.LineBox(text_widget), "green")
        super().__init__(widget)


class ListText(mixins.IgnoreKeyPressMixin, urwid.Text):
    def __init__(self, text, align="center"):
        super().__init__(text, align=align)


class RowDivider(urwid.WidgetWrap):
    def __init__(self, attr_map="default", div_char="-"):
        widget = urwid.AttrMap(urwid.Divider(div_char), attr_map)
        super().__init__(widget)

def color_to_hex(color):
    """
    Given either an hexadecimal or HTML color name, return a the hex
    approximation without the `#`.
    """
    if color.startswith("#"):
        return color.strip("#")
    else:
        return x256.from_html_color_name(color)


