# -*- coding: utf-8 -*-

"""
taiga_ncurses.ui.widgets.issues
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import urwid

from taiga_ncurses import data

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
    on_issue_status_change = None
    on_issue_priority_change = None
    on_issue_severity_change = None
    on_issue_assigned_to_change = None

    def __init__(self, project):
        self.project = project

        self.list_walker = urwid.SimpleFocusListWalker([
            generic.ListText("No issues yet"),
        ])
        self.widget = urwid.ListBox(self.list_walker)
        super().__init__(self.widget)

    def populate(self, issues):
        if issues:
            self.reset()

        for issue in issues:
            self.list_walker.append(IssueEntry(issue, self.project, self.on_issue_status_change,
                                               self.on_issue_priority_change, self.on_issue_severity_change,
                                               self.on_issue_assigned_to_change))

        if len(issues) > 0:
            self.list_walker.set_focus(0)

    def reset(self):
        self.list_walker.clear()


class IssuesListHeader(urwid.WidgetWrap):
    def __init__(self):
        self.issue_button = generic.PlainButton("Issue")
        self.status_button = generic.PlainButton("Status")
        self.priority_button = generic.PlainButton("Priority")
        self.severity_buttton = generic.PlainButton("Severity")
        self.assigned_to_button = generic.PlainButton("Assigned to")

        colum_items = [("weight", 0.5, generic.ButtonCell(self.issue_button))]
        colum_items.append(("weight", 0.1, generic.ButtonCell(self.status_button)))
        colum_items.append(("weight", 0.1, generic.ButtonCell(self.priority_button)))
        colum_items.append(("weight", 0.1, generic.ButtonCell(self.severity_buttton)))
        colum_items.append(("weight", 0.15, generic.ButtonCell(self.assigned_to_button)))

        self.widget = urwid.Columns(colum_items)
        super().__init__(self.widget)


class IssueEntry(urwid.WidgetWrap):
    def __init__(self, issue, project, on_status_change=None, on_priority_change=None, on_severity_change=None,
                 on_assigned_to_change=None):
        self.issue = issue

        issue_ref_and_name = "#{0: <4} {1}".format(str(data.issue_ref(issue)), data.issue_subject(issue))

        colum_items = [("weight", 0.5, generic.ListText(issue_ref_and_name, align="left"))]

        issue_statuses = data.issue_statuses(project)
        items = tuple(((urwid.AttrSpec("h{0}".format(utils.color_to_hex(s.get("color", "#ffffff"))), "default"),
                        s.get("name", "")), s.get("id", None)) for s in issue_statuses.values())
        selected = issue.get("status", None) or project.get("default_issue_status", None)
        status_combo = generic.ComboBox(items, selected_value=selected, style="cyan", enable_markup=True,
                                        on_state_change=on_status_change, user_data=issue)
        colum_items.append(("weight", 0.1, status_combo))

        issue_priorities = data.priorities(project)
        items = tuple(((urwid.AttrSpec("h{0}".format(utils.color_to_hex(s.get("color", "#ffffff"))), "default"),
                        s.get("name", "")), s.get("id", None)) for s in issue_priorities.values())
        selected = issue.get("priority", None) or project.get("default_priority", None)
        priority_combo = generic.ComboBox(items, selected_value=selected, style="cyan", enable_markup=True,
                                        on_state_change=on_priority_change, user_data=issue)
        colum_items.append(("weight", 0.1, priority_combo))

        issue_severities = data.severities(project)
        items = tuple(((urwid.AttrSpec("h{0}".format(utils.color_to_hex(s.get("color", "#ffffff"))), "default"),
                        s.get("name", "")), s.get("id", None)) for s in issue_severities.values())
        selected = issue.get("severity", None) or project.get("default_severity", None)
        severity_combo = generic.ComboBox(items, selected_value=selected, style="cyan", enable_markup=True,
                                        on_state_change=on_severity_change, user_data=issue)
        colum_items.append(("weight", 0.1, severity_combo))

        memberships = [{"user": None, "full_name": "Unassigned"}] + list(data.active_memberships(project).values())
        items = tuple(((urwid.AttrSpec("h{0}".format(utils.color_to_hex(s.get("color", "#ffffff"))), "default"),
                        s.get("full_name", "")), s.get("user", None)) for s in memberships)
        selected = issue.get("assigned_to", None)
        assigned_to_combo = generic.ComboBox(items, selected_value=selected, style="cyan", enable_markup=True,
                                        on_state_change=on_assigned_to_change, user_data=issue)
        colum_items.append(("weight", 0.15, assigned_to_combo))

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
            self._form_inputs(),
            generic.box_solid_fill(" ", 2),
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

    def _form_inputs(self):
        contents = [
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
            # TODO
            #generic.box_solid_fill(" ", 1),
            #self._tags_input(),
        ]

        list_walker = urwid.SimpleFocusListWalker(contents)
        list_walker.set_focus(0)
        return urwid.BoxAdapter(urwid.ListBox(list_walker), 20)

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
        members = [{"user": "null", "full_name": "Unassigned"}] + list(data.active_memberships(self.project).values())
        max_length = max([len(data.user_full_name(s)) for s in members])
        selected_filters = self._filters.get("assigned_to", set())

        self._assigned_to_group = []
        for item in members:
            state = item["user"] in selected_filters

            color = utils.color_to_hex(data.color(item))
            attr = urwid.AttrSpec("h{0}".format(color), "default")

            self._assigned_to_group.append(urwid.CheckBox((attr, data.user_full_name(item)), state, False,
                                                          self._handle_filter_change, ("assigned_to",
                                                          item["user"])))

        colum_items = [(16, urwid.Padding(generic.ListText("Assigned To", align="right"), right=2))]
        colum_items.append(generic.Grid(self._assigned_to_group, 4 + max_length, 3, 0, "left"))
        return urwid.Columns(colum_items)

    def _created_by_input(self):
        members = data.active_memberships(self.project)
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

class IssueForm(mixins.FormMixin, urwid.WidgetWrap):
    _type_combo = None
    _status_combo = None
    _priority_combo = None
    _severity_combo = None
    _assigned_to_combo = None

    def __init__(self, project, issue={}):
        self.project = project
        self.issue = issue

        contents = [
            generic.box_solid_fill(" ", 2),
            self._form_inputs(),
            generic.box_solid_fill(" ", 2),
            self._buttons(),
            generic.box_solid_fill(" ", 1),
        ]
        self.widget = urwid.Pile(contents)

        title = "Edit Issue" if self.issue else "Create Issue"
        super().__init__(urwid.AttrMap(urwid.LineBox(urwid.Padding(self.widget, right=2, left=2),
                                                     title), "popup"))

    @property
    def subject(self):
        return self._subject_edit.get_edit_text()

    @property
    def type(self):
        return self._type_combo.get_selected().value

    @property
    def status(self):
        return self._status_combo.get_selected().value

    @property
    def priority(self):
        return self._priority_combo.get_selected().value

    @property
    def severity(self):
        return self._severity_combo.get_selected().value

    @property
    def assigned_to(self):
        return self._assigned_to_combo.get_selected().value

    @property
    def tags(self):
        tags = self._tags_edit.get_edit_text()
        return tags.split(" ,") if tags else []

    @property
    def description(self):
        return self._description_edit.get_edit_text()

    def _form_inputs(self):
        contents = [
            self._subject_input(),
            generic.box_solid_fill(" ", 1),
            self._type_input(),
            generic.box_solid_fill(" ", 1),
            self._status_input(),
            generic.box_solid_fill(" ", 1),
            self._priority_input(),
            generic.box_solid_fill(" ", 1),
            self._severity_input(),
            generic.box_solid_fill(" ", 1),
            self._assigned_to_input(),
            generic.box_solid_fill(" ", 1),
            self._tags_input(),
            generic.box_solid_fill(" ", 1),
            self._description_input(),
        ]

        list_walker = urwid.SimpleFocusListWalker(contents)
        list_walker.set_focus(0)
        return urwid.BoxAdapter(urwid.ListBox(list_walker), 15)

    def _subject_input(self):
        self._subject_edit = urwid.Edit(edit_text=self.issue.get("subject", ""))

        colum_items = [(17, urwid.Padding(generic.ListText("Subject", align="right"), right=4))]
        colum_items.append(urwid.AttrMap(self._subject_edit, "popup-editor"))
        return urwid.Columns(colum_items)

    def _type_input(self):
        issue_types = data.issue_types(self.project)
        items = tuple(((urwid.AttrSpec("h{0}".format(utils.color_to_hex(s.get("color", "#ffffff"))), "default"),
                        s.get("name", "")), s.get("id", None)) for s in issue_types.values())
        selected = self.issue.get("type", None) or self.project.get("default_issue_type", None)

        self._type_combo = generic.ComboBox(items, selected_value=selected, style="cyan")

        colum_items = [(17, urwid.Padding(generic.ListText("Type", align="right"), right=4))]
        colum_items.append(self._type_combo)
        return urwid.Columns(colum_items)

    def _status_input(self):
        issue_statuses = data.issue_statuses(self.project)
        items = tuple(((urwid.AttrSpec("h{0}".format(utils.color_to_hex(s.get("color", "#ffffff"))), "default"),
                        s.get("name", "")), s.get("id", None)) for s in issue_statuses.values())
        selected = self.issue.get("status", None) or self.project.get("default_issue_status", None)

        self._status_combo = generic.ComboBox(items, selected_value=selected, style="cyan")

        colum_items = [(17, urwid.Padding(generic.ListText("Status", align="right"), right=4))]
        colum_items.append(self._status_combo)
        return urwid.Columns(colum_items)

    def _priority_input(self):
        issue_priorities = data.priorities(self.project)
        items = tuple(((urwid.AttrSpec("h{0}".format(utils.color_to_hex(s.get("color", "#ffffff"))), "default"),
                        s.get("name", "")), s.get("id", None)) for s in issue_priorities.values())
        selected = self.issue.get("priority", None) or self.project.get("default_priority", None)

        self._priority_combo = generic.ComboBox(items, selected_value=selected, style="cyan")

        colum_items = [(17, urwid.Padding(generic.ListText("Priority", align="right"), right=4))]
        colum_items.append(self._priority_combo)
        return urwid.Columns(colum_items)

    def _severity_input(self):
        issue_severities = data.severities(self.project)
        items = tuple(((urwid.AttrSpec("h{0}".format(utils.color_to_hex(s.get("color", "#ffffff"))), "default"),
                        s.get("name", "")), s.get("id", None)) for s in issue_severities.values())
        selected = self.issue.get("severity", None) or self.project.get("default_severity", None)

        self._severity_combo = generic.ComboBox(items, selected_value=selected, style="cyan")

        colum_items = [(17, urwid.Padding(generic.ListText("Severity", align="right"), right=4))]
        colum_items.append(self._severity_combo)
        return urwid.Columns(colum_items)

    def _assigned_to_input(self):
        memberships = [{"user": None, "full_name": "Unassigned"}] + list(data.active_memberships(self.project).values())
        items = tuple(((urwid.AttrSpec("h{0}".format(utils.color_to_hex(s.get("color", "#ffffff"))), "default"),
                        s.get("full_name", "")), s.get("user", None)) for s in memberships)
        selected = self.issue.get("assigned_to", None)

        self._assigned_to_combo = generic.ComboBox(items, selected_value=selected, style="cyan")

        colum_items = [(17, urwid.Padding(generic.ListText("Assigned to", align="right"), right=4))]
        colum_items.append(self._assigned_to_combo)
        return urwid.Columns(colum_items)

    def _tags_input(self):
        self._tags_edit = urwid.Edit(edit_text=", ".join(self.issue.get("tags", [])))

        colum_items = [(17, urwid.Padding(generic.ListText("Tags", align="right"), right=4))]
        colum_items.append(urwid.AttrMap(self._tags_edit, "popup-editor"))
        return urwid.Columns(colum_items)

    def _description_input(self):
        self._description_edit = urwid.Edit(multiline=True, edit_text=self.issue.get("description", ""))

        colum_items = [(17, urwid.Padding(generic.ListText("Description", align="right"), right=4))]
        colum_items.append(urwid.AttrMap(self._description_edit, "popup-editor"))
        return urwid.Columns(colum_items)

    def _buttons(self):
        self.save_button = generic.PlainButton("Save")
        self.cancel_button = generic.PlainButton("Cancel")

        colum_items = [("weight", 1, urwid.Text(""))]
        colum_items.append((15, urwid.AttrMap(urwid.Padding(self.save_button, right=2, left=2),
                                              "popup-submit-button")))
        colum_items.append((2, urwid.Text(" ")))
        colum_items.append((15, urwid.AttrMap(urwid.Padding(self.cancel_button, right=1, left=2),
                                              "popup-cancel-button")))
        return urwid.Columns(colum_items)
