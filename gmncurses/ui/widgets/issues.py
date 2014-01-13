# -*- coding: utf-8 -*-

"""
gmncurses.ui.widgets.issues
~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import urwid

from gmncurses import data

from . import mixins, generic, utils


class IssuesStats(urwid.WidgetWrap):
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


class IssuesFiltersInfo(urwid.WidgetWrap):
    def __init__(self, project, filters):
        self.project = project
        self.filters = filters

        self.entries = urwid.Text("None")
        self.widget = urwid.Columns([
            (12, urwid.Text(("cyan", "Filter by:"))),
            self.entries
        ])
        self._refresh()

        super().__init__(self.widget)

    def set_filters(self, filters):
        self.filters = filters
        self._refresh()

    def _refresh(self):
        # TODO: I don't like this method I should to refactor it, when I have more time
        contents = []
        for filter_type, values in self.filters.items():
            if filter_type == "type":
                if values:
                    contents.append(("default", "TYPE: "))
                for value in values:
                    hex_color, type = data.issue_type_with_color({filter_type: value}, self.project)
                    color = utils.color_to_hex(hex_color)
                    attr = urwid.AttrSpec("h{0}".format(color), "default")
                    contents.append((attr, "{} ".format(type)))

            elif filter_type == "status":
                if values:
                    contents.append(("default", "STATUS: "))
                for value in values:
                    hex_color, status = data.issue_status_with_color({filter_type: value}, self.project)
                    color = utils.color_to_hex(hex_color)
                    attr = urwid.AttrSpec("h{0}".format(color), "default")
                    contents.append((attr, "{} ".format(status)))

            elif filter_type == "priority":
                if values:
                    contents.append(("default", "PRIORITY: "))
                for value in values:
                    hex_color, priority = data.issue_priority_with_color({filter_type: value}, self.project)
                    color = utils.color_to_hex(hex_color)
                    attr = urwid.AttrSpec("h{0}".format(color), "default")
                    contents.append((attr, "{} ".format(priority)))

            elif filter_type == "severity":
                if values:
                    contents.append(("default", "SEVERITY: "))
                for value in values:
                    hex_color, severity = data.issue_severity_with_color({filter_type: value}, self.project)
                    color = utils.color_to_hex(hex_color)
                    attr = urwid.AttrSpec("h{0}".format(color), "default")
                    contents.append((attr, "{} ".format(severity)))

            elif filter_type == "assigned_to":
                if values:
                    contents.append(("default", "ASSIGNED TO: "))
                for value in values:
                    hex_color, assigned_to = data.issue_assigned_to_with_color({filter_type: value}, self.project)
                    color = utils.color_to_hex(hex_color)
                    attr = urwid.AttrSpec("h{0}".format(color), "default")
                    contents.append((attr, "{} ".format(assigned_to)))

            elif filter_type == "owner":
                if values:
                    contents.append(("default", "CREATED BY: "))
                for value in values:
                    hex_color, owner = data.issue_owner_with_color({filter_type: value}, self.project)
                    color = utils.color_to_hex(hex_color)
                    attr = urwid.AttrSpec("h{0}".format(color), "default")
                    contents.append((attr, "{} ".format(owner)))

            elif filter_type == "tags":
                if values:
                    contents.append(("default", "TAG: "))
                #TODO: When I added tags to the filters_popup
                pass

            else:
                contents.append(("default", "  unknown filter '{}'".format(filter_type)))

        if not contents:
            contents = ("default", "No filter selected")

        self.entries.set_text(contents)


class IssuesList(mixins.ViMotionMixin, mixins.EmacsMotionMixin, urwid.WidgetWrap):
    def __init__(self, project):
        self.project = project

        self.header = IssuesListHeader()

        self.widget = urwid.Pile([self.header])
        super().__init__(self.widget)

    def populate(self, issues):
        if issues:
            self.reset()

        first_gains_focus = len(self.widget.contents) == 1 and issues

        for issue in issues:
            self.widget.contents.append((IssueEntry(issue, self.project),
                                         ("weight", 0.1)))

        if first_gains_focus:
            self.widget.contents.focus = 1

    def reset(self):
        self.widget.contents = self.widget.contents[:1]


class IssuesListHeader(urwid.WidgetWrap):
    def __init__(self):
        self.issue_button = generic.PlainButton("Issue")
        self.status_button = generic.PlainButton("Status")
        self.priority_button = generic.PlainButton("Priority")
        self.severity_buttton = generic.PlainButton("Severity")
        self.assigned_to_button = generic.PlainButton("Assigned to")

        colum_items = [("weight", 0.55, generic.ButtonCell(self.issue_button))]
        colum_items.append(("weight", 0.1, generic.ButtonCell(self.status_button)))
        colum_items.append(("weight", 0.1, generic.ButtonCell(self.priority_button)))
        colum_items.append(("weight", 0.1, generic.ButtonCell(self.severity_buttton)))
        colum_items.append(("weight", 0.15, generic.ButtonCell(self.assigned_to_button)))

        self.widget = urwid.Columns(colum_items)
        super().__init__(self.widget)


class IssueEntry(urwid.WidgetWrap):
    def __init__(self, issue, project):
        issue_ref_and_name = "#{0: <4} {1}".format(str(data.issue_ref(issue)), data.issue_subject(issue))

        colum_items = [("weight", 0.55, generic.ListText(issue_ref_and_name, align="left"))]

        hex_color, status = data.issue_status_with_color(issue, project)
        color = utils.color_to_hex(hex_color)
        attr = urwid.AttrSpec("h{0}".format(color), "default")
        colum_items.append(("weight", 0.1, generic.ListText((attr, status))))

        hex_color, priority = data.issue_priority_with_color(issue, project)
        color = utils.color_to_hex(hex_color)
        attr = urwid.AttrSpec("h{0}".format(color), "default")
        colum_items.append(("weight", 0.1, generic.ListText((attr, priority))))

        hex_color, severity = data.issue_severity_with_color(issue, project)
        color = utils.color_to_hex(hex_color)
        attr = urwid.AttrSpec("h{0}".format(color), "default")
        colum_items.append(("weight", 0.1, generic.ListText((attr, severity))))

        hex_color, username =  data.issue_assigned_to_with_color(issue, project)
        color = utils.color_to_hex(hex_color)
        attr = urwid.AttrSpec("h{0}".format(color), "default")
        colum_items.append(("weight", 0.15, generic.ListText((attr, username))))

        self.widget = urwid.Columns(colum_items)
        super().__init__(urwid.AttrMap(self.widget, "default", "focus"))

    def selectable(self):
        return True


class FiltersPopup(mixins.FormMixin, urwid.WidgetWrap):
    _filters = {
        "type": set(),
        "status": set(),
        "priority": set(),
        "severity": set(),
        "assigned_to": set(),
        "owner": set(),
        "tags": set()
    }

    def __init__(self, project, filters={}):
        self.project = project

        if filters:
            self._filters = filters

        contents = [
            generic.box_solid_fill(" ", 2),
            self._types_input(),
            generic.box_solid_fill(" ", 1),
            self._statuses_input(),
            generic.box_solid_fill(" ", 1),
            self._priorities_input(),
            generic.box_solid_fill(" ", 1),
            self._severities_input(),
            generic.box_solid_fill(" ", 1),
            self._assigned_to_input(),
            generic.box_solid_fill(" ", 1),
            self._created_by_input(),
            generic.box_solid_fill(" ", 1),
            # TODO
            #self._tags_input(),
            #generic.box_solid_fill(" ", 2),
            self._buttons(),
            generic.box_solid_fill(" ", 1)
        ]
        self.widget = urwid.Pile(contents)

        title = "Filter issues by..."
        super().__init__(urwid.AttrMap(urwid.LineBox(urwid.Padding(self.widget, right=2, left=2),
                                                     title), "popup"))

    @property
    def filters(self):
        return self._filters

    def _handle_filter_change(self, check_box, new_state, data):
        filter_type, value = data

        if new_state:
            self._filters[filter_type].add(value)
        else:
            self._filters[filter_type].difference_update({value})

    def _types_input(self):
        issue_types = data.issue_types(self.project)
        max_length = max([len(s["name"]) for s in issue_types.values()])
        selected_filters = self._filters.get("type", set())

        self._issue_types_group = []
        for id, item in issue_types.items():
            state = id in selected_filters

            color = utils.color_to_hex(data.color(item))
            attr = urwid.AttrSpec("h{0}".format(color), "default")

            self._issue_types_group.append(urwid.CheckBox((attr, item["name"]), state, False,
                                                          self._handle_filter_change, ("type", id)))

        colum_items = [(16, urwid.Padding(generic.ListText("Types", align="right"), right=2))]
        colum_items.append(generic.Grid(self._issue_types_group, 4 + max_length, 3, 0, "left"))
        return urwid.Columns(colum_items)

    def _statuses_input(self):
        issue_statuses = data.issue_statuses(self.project)
        max_length = max([len(s["name"]) for s in issue_statuses.values()])
        selected_filters = self._filters.get("status", set())

        self._issue_statuses_group = []
        for id, item in issue_statuses.items():
            state = id in selected_filters

            color = utils.color_to_hex(data.color(item))
            attr = urwid.AttrSpec("h{0}".format(color), "default")

            self._issue_statuses_group.append(urwid.CheckBox((attr, item["name"]), state, False,
                                                             self._handle_filter_change, ("status", id)))

        colum_items = [(16, urwid.Padding(generic.ListText("Statuses", align="right"), right=2))]
        colum_items.append(generic.Grid(self._issue_statuses_group, 4 + max_length, 3, 0, "left"))
        return urwid.Columns(colum_items)

    def _priorities_input(self):
        priorities = data.priorities(self.project)
        max_length = max([len(s["name"]) for s in priorities.values()])
        selected_filters = self._filters.get("priority", set())

        self._priorities_group = []
        for id, item in priorities.items():
            state = id in selected_filters

            color = utils.color_to_hex(data.color(item))
            attr = urwid.AttrSpec("h{0}".format(color), "default")

            self._priorities_group.append(urwid.CheckBox((attr, item["name"]), state, False,
                                                         self._handle_filter_change, ("priority", id)))

        colum_items = [(16, urwid.Padding(generic.ListText("Priorities", align="right"), right=2))]
        colum_items.append(generic.Grid(self._priorities_group, 4 + max_length, 3, 0, "left"))
        return urwid.Columns(colum_items)

    def _severities_input(self):
        severities = data.severities(self.project)
        max_length = max([len(s["name"]) for s in severities.values()])
        selected_filters = self._filters.get("severity", set())

        self._severities_group = []
        for id, item in severities.items():
            state = id in selected_filters

            color = utils.color_to_hex(data.color(item))
            attr = urwid.AttrSpec("h{0}".format(color), "default")

            self._severities_group.append(urwid.CheckBox((attr, item["name"]), state, False,
                                                         self._handle_filter_change, ("severity", id)))

        colum_items = [(16, urwid.Padding(generic.ListText("Severities", align="right"), right=2))]
        colum_items.append(generic.Grid(self._severities_group, 4 + max_length, 3, 0, "left"))
        return urwid.Columns(colum_items)

    def _assigned_to_input(self):
        members = data.memberships(self.project)
        max_length = max([len(data.user_full_name(s)) for s in members.values()])
        selected_filters = self._filters.get("assigned_to", set())

        self._assigned_to_group = []
        for id, item in members.items():
            state = id in selected_filters

            color = utils.color_to_hex(data.color(item))
            attr = urwid.AttrSpec("h{0}".format(color), "default")

            self._assigned_to_group.append(urwid.CheckBox((attr, data.user_full_name(item)), state, False,
                                                          self._handle_filter_change, ("assigned_to", id)))

        colum_items = [(16, urwid.Padding(generic.ListText("Assigned To", align="right"), right=2))]
        colum_items.append(generic.Grid(self._assigned_to_group, 4 + max_length, 3, 0, "left"))
        return urwid.Columns(colum_items)

    def _created_by_input(self):
        members = data.memberships(self.project)
        max_length = max([len(data.user_full_name(s)) for s in members.values()])
        selected_filters = self._filters.get("owner", set())

        self._created_by_group = []
        for id, item in members.items():
            state = id in selected_filters

            color = utils.color_to_hex(data.color(item))
            attr = urwid.AttrSpec("h{0}".format(color), "default")

            self._created_by_group.append(urwid.CheckBox((attr, data.user_full_name(item)), state, False,
                                                         self._handle_filter_change, ("owner", id)))

        colum_items = [(16, urwid.Padding(generic.ListText("Created By", align="right"), right=2))]
        colum_items.append(generic.Grid(self._created_by_group, 4 + max_length, 3, 0, "left"))
        return urwid.Columns(colum_items)

    def _tags_input(self):
        # TODO:
        max_length = 10

        self._tags_group = []

        colum_items = [(16, urwid.Padding(generic.ListText("Tags", align="right"), right=2))]
        colum_items.append(generic.Grid(self._tags_group, 4 + max_length, 3, 0, "left"))
        return urwid.Columns(colum_items)

    def _buttons(self):
        self.filter_button = generic.PlainButton("Filter")
        self.cancel_button = generic.PlainButton("Cancel")

        colum_items = [("weight", 1, urwid.Text(""))]
        colum_items.append((15, urwid.AttrMap(urwid.Padding(self.filter_button, right=2, left=2),
                                              "popup-submit-button")))
        colum_items.append((2, urwid.Text(" ")))
        colum_items.append((15, urwid.AttrMap(urwid.Padding(self.cancel_button, right=1, left=2),
                                              "popup-cancel-button")))
        return urwid.Columns(colum_items)
