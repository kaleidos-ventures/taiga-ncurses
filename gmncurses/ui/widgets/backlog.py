# -*- coding: utf-8 -*-

"""
gmncurses.ui.widgets.backlog
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import urwid

from gmncurses import data

from . import mixins, generic, utils


class BacklogStats(urwid.WidgetWrap):
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
            ("weight", 0.2, urwid.Pile([TotalPoints(project_stats), TotalMilestones(self.project)])),
            ("weight", 0.3, urwid.Pile([CompletedMilestones(self.project), CurrentMilestone(self.project)])),
            ("weight", 0.6, urwid.Pile([ClosedPoints(project_stats), DefinedPoints(project_stats)])),
        ])


class TotalPoints(urwid.Text):
    def __init__(self, project_stats):
        text = ["Total points: ", ("cyan", str(data.total_points(project_stats)))]
        super().__init__(text)


class TotalMilestones(urwid.Text):
    def __init__(self, project):
        text = ["Total sprints: ", ("cyan", str(data.total_sprints(project)))]
        super().__init__(text)


class ClosedPoints(urwid.Columns):
    def __init__(self, project_stats, **kwargs):
        text = urwid.Text(["Closed points: ", ("green", str(data.closed_points(project_stats)))])

        progressbar = urwid.ProgressBar("progressbar-normal", "progressbar-complete",
                                        data.closed_points(project_stats), data.total_points(project_stats),
                                        "progressbar-smooth")

        widget_list = [("weight", 0.4, text),
                       ("weight", 0.6, urwid.Padding(progressbar, align='center', left=2, right=2))]
        super().__init__(widget_list, **kwargs)


class DefinedPoints(urwid.Columns):
    def __init__(self, project_stats, **kwargs):
        defined_points_percentage = data.defined_points_percentage(project_stats)
        if defined_points_percentage <= 100.0:
            text = urwid.Text(["Defined points: ", ("red", str(data.defined_points(project_stats)))])
        else:
            text = urwid.Text(["Defined points: ", ("red", str(data.defined_points(project_stats))),
                               " (", ("red", "+{0:.1f} %".format(defined_points_percentage - 100.0)), ")"])

        progressbar = urwid.ProgressBar("progressbar-normal-red", "progressbar-complete-red",
                                        data.defined_points(project_stats), data.total_points(project_stats),
                                        "progressbar-smooth-red")

        widget_list = [("weight", 0.4, text),
                       ("weight", 0.6, urwid.Padding(progressbar, align='center', left=2, right=2))]
        super().__init__(widget_list, **kwargs)


class CurrentMilestone(urwid.Text):
    def __init__(self, project):
        text = [
            "Current sprint: ",
            ("cyan", str(data.current_sprint(project))),
            " (",
            ("cyan", str(data.current_sprint_name(project))),
            ")",
        ]
        super().__init__(text)


class CompletedMilestones(urwid.Text):
    def __init__(self, project):
        text = ["Completed sprints: ", ("green", str(len(data.completed_sprints(project))))]
        super().__init__(text)


class UserStoryList(mixins.ViMotionMixin, mixins.EmacsMotionMixin, urwid.WidgetWrap):
    def __init__(self, project):
        self.project = project
        self.roles = data.computable_roles(project)

        colum_items = [("weight", 0.6, generic.ListCell("US"))]
        colum_items.append(("weight", 0.08, generic.ListCell("Status")))
        colum_items.extend([("weight", 0.05, generic.ListCell(r["name"])) for r in self.roles.values()])
        colum_items.append(("weight", 0.05, generic.ListCell(("green", "TOTAL"))))
        colum_items.append(("weight", 0.05, generic.ListCell(("cyan", "SUM."))))

        columns = urwid.Columns(colum_items)
        self.widget = urwid.Pile([columns])
        super().__init__(self.widget)

    def populate(self, user_stories, project_stats, set_focus=None):
        if user_stories:
            self.reset()

        self.doomline_limit = data.doomline_limit_points(project_stats)
        first_gains_focus = len(self.widget.contents) == 1 and user_stories

        summation = 0
        doomline = False

        for us in user_stories:
            summation += data.us_total_points(us)

            if not doomline and summation > self.doomline_limit:
                self.widget.contents.append((generic.RowDivider("red", div_char="☠"), ("weight", 0.1)))
                doomline = True

            self.widget.contents.append((UserStoryEntry(us, self.project, self.roles, summation),
                                         ("weight", 0.1)))
        # Set the focus # TODO: Refactor
        if first_gains_focus:
            if set_focus:
                for idx, item in enumerate(self.widget.contents):
                    widget, options = item
                    if type(widget) is UserStoryEntry and widget.user_story == set_focus:
                        self.widget.contents.focus = idx

            if not self.widget.contents.focus:
                self.widget.contents.focus = 1


    def reset(self):
        self.widget.contents = self.widget.contents[:1]


class UserStoryEntry(urwid.WidgetWrap):
    def __init__(self, us, project, roles, summation=0.0):
        self.user_story = us

        us_ref_and_name = "#{0: <6} {1}".format(str(data.us_ref(us)), data.us_subject(us))
        colum_items = [("weight", 0.6, generic.ListText(us_ref_and_name, align="left"))]

        hex_color, status = data.us_status_with_color(us, project)
        color = utils.color_to_hex(hex_color)
        attr = urwid.AttrSpec("h{0}".format(color), "default")
        colum_items.append(("weight", 0.08, generic.ListText( (attr, status) )))

        points_by_role = data.us_points_by_role(us, project, roles.values())
        for point in points_by_role:
            colum_items.append(("weight", 0.05, generic.ListText(str(point))))
        colum_items.append(("weight", 0.05, generic.ListText(("green", "{0:.1f}".format(
                                                                        data.us_total_points(us))))))
        colum_items.append(("weight", 0.05, generic.ListText(("cyan", "{0:.1f}".format(summation)))))

        self.widget = urwid.Columns(colum_items)
        super().__init__(urwid.AttrMap(self.widget, "default", "focus"))

    def selectable(self):
        return True

class UserStoryForm( mixins.FormMixin, urwid.WidgetWrap):
    _status = None
    _points = {}

    def __init__(self, project, user_story={}):
        self.project = project
        self.user_story = user_story

        contents = [
            generic.box_solid_fill(" ", 2),
            self._subject_input(),
            generic.box_solid_fill(" ", 1),
            self._points_input(),
            generic.box_solid_fill(" ", 1),
            self._status_input(),
            generic.box_solid_fill(" ", 1),
            self._tags_input(),
            generic.box_solid_fill(" ", 1),
            self._description_input(),
            generic.box_solid_fill(" ", 1),
            self._requirements_input(),
            generic.box_solid_fill(" ", 2),
            self._buttons(),
            generic.box_solid_fill(" ", 1),
        ]
        self.widget = urwid.Pile(contents)

        title = "Edit User Story" if self.user_story else "Create User Story"
        super().__init__(urwid.AttrMap(urwid.LineBox(urwid.Padding(self.widget, right=2, left=2),
                                                     title), "popup"))

    @property
    def subject(self):
        return self._subject_edit.get_edit_text()

    @property
    def points(self):
        return self._points

    @property
    def status(self):
        return self._status

    @property
    def tags(self):
        tags = self._tags_edit.get_edit_text()
        return tags.split(" ,") if tags else []

    @property
    def description(self):
        return self._description_edit.get_edit_text()

    @property
    def team_requirement(self):
        return self._team_requirement_checkbox.get_state()

    @property
    def client_requirement(self):
        return self._client_requirement_checkbox.get_state()

    def _subject_input(self):
        self._subject_edit = urwid.Edit(edit_text=self.user_story.get("subject", ""))

        colum_items = [(17, urwid.Padding(generic.ListText("Subject", align="right"), right=4))]
        colum_items.append(urwid.AttrMap(self._subject_edit, "popup-editor"))
        return urwid.Columns(colum_items)

    def _points_input(self):
        roles = data.computable_roles(self.project)
        points = data.points(self.project)
        max_length = max([len(s.get("name", "")) for s in points.values()])

        self._role_points_groups = {}

        points_pile = []
        for r_id, role in roles.items():
            self._points[r_id] = (self.user_story.get("points", {}).get(r_id, None) or
                                  self.project.get("default_points", None))

            points_colum = [(17, urwid.Text(role["name"]))]
            points_group = []
            for p_id, point in points.items():
                urwid.RadioButton(points_group, point.get("name", "") or str(point.get("value", 0)),
                                  state=(int(p_id) == self.user_story.get("points", {}).get(r_id, None) or
                                         int(p_id) == self.project.get("default_points", None)),
                                  on_state_change=self._handler_point_radiobutton_change,
                                  user_data={r_id:point["id"]})

            points_colum.append(generic.Grid(points_group, 4 + max_length, 2, 0, "left"))
            points_pile.append(urwid.Columns(points_colum))

            self._role_points_groups[r_id] = points_group

        self._points_checkbox = urwid.Pile(points_pile)

        colum_items = [(17, urwid.Padding(generic.ListText("Points", align="right"), right=4))]
        colum_items.append(self._points_checkbox)
        return urwid.Columns(colum_items)

    def _handler_point_radiobutton_change(self, radio_button, new_state, user_data):
        if new_state:
            self._points.update(user_data)

    def _status_input(self):
        self._status = self.user_story.get("status", None) or self.project.get("default_us_status", None)

        us_statuses = data.us_statuses(self.project)
        max_length = max([len(s["name"]) for s in us_statuses.values()])

        self._us_status_group = []
        for s_id, status in us_statuses.items():
            urwid.RadioButton(self._us_status_group, status["name"],
                              state=(status["id"] == self.user_story.get("status", None) or
                                     status["id"] == self.project.get("default_us_status", None)),
                              on_state_change=self._handler_status_radiobutton_change,
                              user_data=status["id"])

        colum_items = [(17, urwid.Padding(generic.ListText("Status", align="right"), right=4))]
        colum_items.append(generic.Grid(self._us_status_group, 4 + max_length, 3, 0, "left"))
        return urwid.Columns(colum_items)

    def _handler_status_radiobutton_change(self, radio_button, new_state, user_data):
        if new_state:
            self._status = user_data

    def _tags_input(self):
        self._tags_edit = urwid.Edit(edit_text=", ".join(self.user_story.get("tags", [])))

        colum_items = [(17, urwid.Padding(generic.ListText("Tags", align="right"), right=4))]
        colum_items.append(urwid.AttrMap(self._tags_edit, "popup-editor"))
        return urwid.Columns(colum_items)

    def _description_input(self):
        self._description_edit = urwid.Edit(multiline=True, edit_text=self.user_story.get("subject", ""))

        colum_items = [(17, urwid.Padding(generic.ListText("Description", align="right"), right=4))]
        colum_items.append(urwid.AttrMap(self._description_edit, "popup-editor"))
        return urwid.Columns(colum_items)

    def _requirements_input(self):
        self._client_requirement_checkbox = urwid.CheckBox("Client's requirement",
                state=self.user_story.get("client_requirement", False))
        self._team_requirement_checkbox = urwid.CheckBox("Team's requirement",
                state=self.user_story.get("team_requirement", False))

        colum_items = [(17, urwid.Text(" "))]
        colum_items.append(self._client_requirement_checkbox)
        colum_items.append(self._team_requirement_checkbox)
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
