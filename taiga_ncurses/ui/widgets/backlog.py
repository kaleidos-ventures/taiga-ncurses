# -*- coding: utf-8 -*-

"""
taiga_ncurses.ui.widgets.backlog
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import urwid

from taiga_ncurses import data

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
        text = ["Total milestones: ", ("cyan", str(data.total_milestones(project)))]
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
            "Current milestone: ",
            ("cyan", str(data.current_milestone_name(project))),
        ]
        super().__init__(text)


class CompletedMilestones(urwid.Text):
    def __init__(self, project):
        text = ["Completed milestones: ", ("green", str(len(data.completed_milestones(project))))]
        super().__init__(text)


class UserStoryList(mixins.ViMotionMixin, mixins.EmacsMotionMixin, urwid.WidgetWrap):
    on_user_story_status_change = None
    on_user_story_points_change = None

    def __init__(self, project):
        self.project = project
        self.roles = data.computable_roles(project)

        colum_items = [("weight", 0.5, generic.ListCell("US"))]
        colum_items.append(("weight", 0.15, generic.ListCell("Status")))
        colum_items.extend([("weight", 0.05, generic.ListCell(r["name"])) for r in self.roles.values()])
        colum_items.append(("weight", 0.05, generic.ListCell(("green", "TOTAL"))))
        colum_items.append(("weight", 0.08, generic.ListCell(("cyan", "SUM."))))

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

            self.widget.contents.append((UserStoryEntry(us, self.project, self.roles, summation,
                                                        self.on_user_story_status_change,
                                                        self.on_user_story_points_change),
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
    def __init__(self, us, project, roles, summation=0.0, on_status_change=None, on_points_change=None):
        self.user_story = us

        colum_items = [(6, generic.ListText("#{0}".format(str(data.us_ref(us))), align="left"))]

        colum_items.append((1, urwid.AttrMap(generic.ListText("⊕" if data.us_client_requirement(us) else " ",
                                                              align="left"), "yellow", "focus")))
        colum_items.append((1, urwid.AttrMap(generic.ListText("☂" if data.us_team_requirement(us) else " ",
                                                              align="left"), "cyan", "focus")))
        colum_items.append((2, urwid.AttrMap(generic.ListText("✖" if data.us_is_blocked(us) else " ",
                                                              align="left"), "red", "focus")))

        colum_items.append(("weight", 0.5, generic.ListText(data.us_subject(us), align="left")))

        us_statuses = data.us_statuses(project)
        items = tuple(((urwid.AttrSpec("h{0}".format(utils.color_to_hex(s.get("color", "#ffffff"))), "default"),
                        s.get("name", "")), s.get("id", None)) for s in us_statuses.values())
        selected = us.get("status", None) or project.get("default_us_status", None)
        status_combo = generic.ComboBox(items, selected_value=selected, style="cyan", enable_markup=True,
                                        on_state_change=on_status_change, user_data=us)
        colum_items.append(("weight", 0.15, status_combo))

        points = data.points(project)
        items = tuple((p.get("name", ""), p.get("id", None)) for p in points.values())
        for r_id, role in roles.items():
            selected = (us.get("points", {}).get(r_id, None) or
                        project.get("default_points", None))
            points_combo = generic.ComboBox(items, selected_value=selected, style="cyan",
                                            on_state_change=on_points_change, user_data=(us, r_id))
            colum_items.append(("weight", 0.05, points_combo))

        colum_items.append(("weight", 0.05, generic.ListText(("green", "{0:.1f}".format(
                                                                        data.us_total_points(us))))))
        colum_items.append(("weight", 0.08, generic.ListText(("cyan", "{0:.1f}".format(summation)))))

        self.widget = urwid.Columns(colum_items)
        super().__init__(urwid.AttrMap(self.widget, "default", "focus"))

    def selectable(self):
        return True

class UserStoryForm(mixins.FormMixin, urwid.WidgetWrap):
    _milestone_combo = None
    _status_combo = None
    _points_combos = {}

    def __init__(self, project, user_story={}):
        self.project = project
        self.user_story = user_story

        contents = [
            generic.box_solid_fill(" ", 2),
            self._form_inputs(),
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
    def milestone(self):
        return self._milestone_combo.get_selected().value

    @property
    def points(self):
        return {k: c.get_selected().value for k, c in self._points_combos.items()}

    @property
    def status(self):
        return self._status_combo.get_selected().value

    @property
    def is_blocked(self):
        return self._is_blocked_checkbox.get_state()

    @property
    def blocked_note(self):
        return self._blocked_note_edit.get_edit_text()

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

    def _form_inputs(self):
        contents = [
            self._subject_input(),
            generic.box_solid_fill(" ", 1),
            self._milestone_input(),
            generic.box_solid_fill(" ", 1),
            self._points_input(),
            generic.box_solid_fill(" ", 1),
            self._status_input(),
            generic.box_solid_fill(" ", 1),
            self._is_blocked_input(),
            generic.box_solid_fill(" ", 1),
            self._blocked_note_input(),
            generic.box_solid_fill(" ", 1),
            self._tags_input(),
            generic.box_solid_fill(" ", 1),
            self._description_input(),
            generic.box_solid_fill(" ", 1),
            self._requirements_input(),
        ]

        list_walker = urwid.SimpleFocusListWalker(contents)
        list_walker.set_focus(0)
        return urwid.BoxAdapter(urwid.ListBox(list_walker), 16)

    def _subject_input(self):
        self._subject_edit = urwid.Edit(edit_text=self.user_story.get("subject", ""))

        colum_items = [(17, urwid.Padding(generic.ListText("Subject", align="right"), right=4))]
        colum_items.append(urwid.AttrMap(self._subject_edit, "popup-editor"))
        return urwid.Columns(colum_items)

    def _milestone_input(self):
        milestones = [{"id": None, "name": "None"}] + data.list_of_milestones(self.project)
        items = tuple((m.get("name", ""), m.get("id", None)) for m in milestones)
        selected = self.user_story.get("milestone", None)

        self._milestone_combo = generic.ComboBox(items, selected_value=selected, style="cyan")

        colum_items = [(17, urwid.Padding(generic.ListText("Milestone", align="right"), right=4))]
        colum_items.append(self._milestone_combo)
        return urwid.Columns(colum_items)

    def _points_input(self):
        roles = data.computable_roles(self.project)
        max_role_len = max([len(r["name"]) for r in roles.values()]) + 2

        points = data.points(self.project)
        items = tuple((p.get("name", ""), p.get("id", None)) for p in points.values())

        points_pile_contents = []
        for r_id, role in roles.items():
            selected = (self.user_story.get("points", {}).get(r_id, None) or
                        self.project.get("default_points", None))
            self._points_combos[r_id] = generic.ComboBox(items, selected_value=selected, style="cyan")

            points_pile_contents.append(urwid.Columns([
                (max_role_len, urwid.Text("{}:".format(role["name"]))),
                self._points_combos[r_id]
            ]))

        points_pile = urwid.Pile(points_pile_contents)

        colum_items = [(17, urwid.Padding(generic.ListText("Points", align="right"), right=4))]
        colum_items.append(points_pile)
        return urwid.Columns(colum_items)

    def _status_input(self):
        us_statuses = data.us_statuses(self.project)
        items = tuple(((urwid.AttrSpec("h{0}".format(utils.color_to_hex(s.get("color", "#ffffff"))), "default"),
                        s.get("name", "")), s.get("id", None)) for s in us_statuses.values())
        selected = self.user_story.get("status", None) or self.project.get("default_us_status", None)

        self._status_combo = generic.ComboBox(items, selected_value=selected, style="cyan")

        colum_items = [(17, urwid.Padding(generic.ListText("Status", align="right"), right=4))]
        colum_items.append(self._status_combo)
        return urwid.Columns(colum_items)

    def _is_blocked_input(self):
        self._is_blocked_checkbox = urwid.CheckBox(["Is blocked ", (("popup-text-red"), "✖")],
                state=self.user_story.get("is_blocked", False))

        colum_items = [(17, urwid.Text(" "))]
        colum_items.append(self._is_blocked_checkbox)
        return urwid.Columns(colum_items)

    def _blocked_note_input(self):
        self._blocked_note_edit = urwid.Edit(multiline=True, edit_text=self.user_story.get("blocked_note", ""))

        colum_items = [(17, urwid.Padding(generic.ListText("Blocked note", align="right"), right=4))]
        colum_items.append(urwid.AttrMap(self._blocked_note_edit, "popup-editor"))
        return urwid.Columns(colum_items)

    def _tags_input(self):
        self._tags_edit = urwid.Edit(edit_text=", ".join(self.user_story.get("tags", [])))

        colum_items = [(17, urwid.Padding(generic.ListText("Tags", align="right"), right=4))]
        colum_items.append(urwid.AttrMap(self._tags_edit, "popup-editor"))
        return urwid.Columns(colum_items)

    def _description_input(self):
        self._description_edit = urwid.Edit(multiline=True, edit_text=self.user_story.get("description", ""))

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

class UserStoriesInBulkForm(mixins.FormMixin, urwid.WidgetWrap):

    def __init__(self, project):
        self.project = project

        contents = [
            generic.box_solid_fill(" ", 2),
            self._form_inputs(),
            generic.box_solid_fill(" ", 2),
            self._buttons(),
            generic.box_solid_fill(" ", 1),
        ]
        self.widget = urwid.Pile(contents)

        title = "Create User Stories in bulk"
        super().__init__(urwid.AttrMap(urwid.LineBox(urwid.Padding(self.widget, right=2, left=2),
                                                     title), "popup"))

    @property
    def subjects(self):
        return self._subjects_edit.get_edit_text()

    def _form_inputs(self):
        contents = [
            self._subjects_input(),
        ]

        list_walker = urwid.SimpleFocusListWalker(contents)
        list_walker.set_focus(0)
        return urwid.BoxAdapter(urwid.ListBox(list_walker), 16)

    def _subjects_input(self):
        self._subjects_edit = urwid.Edit(edit_text="", multiline=True, )

        colum_items = [(13, urwid.Padding(generic.ListText("Subjects", align="right"), right=4))]
        colum_items.append(urwid.AttrMap(self._subjects_edit, "popup-editor"))
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


class MIlestoneSelectorPopup(mixins.FormMixin, urwid.WidgetWrap):
    def __init__(self, project, user_story={}):
        self.project = project
        self.user_story = user_story
        self.options = []

        contents = [
            generic.box_solid_fill(" ", 2),
            urwid.Padding(self._description(), right=2, left=2),
            generic.box_solid_fill(" ", 1),
            urwid.Padding(self._milestone_selector(), right=2, left=2),
            generic.box_solid_fill(" ", 2),
            self._buttons(),
            generic.box_solid_fill(" ", 1),
        ]
        self.widget = urwid.Pile(contents)

        title = "Move User Story #{} to a Milestone".format(data.us_ref(self.user_story))
        super().__init__(urwid.AttrMap(urwid.LineBox(urwid.Padding(self.widget, right=2, left=2),
                                                     title), "popup"))

    def _description(self):
        description = "Move US #{0} '{1}' to milestone...".format(data.us_ref(self.user_story),
                                                                  data.us_subject(self.user_story))
        return urwid.Text(description)

    def _milestone_selector(self):
        contents = []
        for milestone in data.list_of_milestones(self.project):
            option = MilestoneOptionEntry(milestone)
            self.options.append(option)

            contents.append(option)
            contents.append(generic.box_solid_fill(" ", 1))

        list_walker = urwid.SimpleFocusListWalker(contents)
        if len(contents) > 0:
            list_walker.set_focus(0)
        return urwid.BoxAdapter(urwid.ListBox(list_walker), 20)

    def _buttons(self):
        self.cancel_button = generic.PlainButton("Cancel")

        colum_items = [("weight", 1, urwid.Text(""))]
        colum_items.append((15, urwid.AttrMap(urwid.Padding(self.cancel_button, right=1, left=2),
                                              "popup-cancel-button")))
        return urwid.Columns(colum_items)

class MIlestoneSelectorPopup(mixins.FormMixin, urwid.WidgetWrap):
    def __init__(self, project, user_story={}):
        self.project = project
        self.user_story = user_story
        self.options = []

        contents = [
            generic.box_solid_fill(" ", 2),
            urwid.Padding(self._description(), right=2, left=2),
            generic.box_solid_fill(" ", 1),
            urwid.Padding(self._milestone_selector(), right=2, left=2),
            generic.box_solid_fill(" ", 2),
            self._buttons(),
            generic.box_solid_fill(" ", 1),
        ]
        self.widget = urwid.Pile(contents)

        title = "Move User Story #{} to a Milestone".format(data.us_ref(self.user_story))
        super().__init__(urwid.AttrMap(urwid.LineBox(urwid.Padding(self.widget, right=2, left=2),
                                                     title), "popup"))

    def _description(self):
        description = "Move US #{0} '{1}' to milestone...".format(data.us_ref(self.user_story),
                                                                  data.us_subject(self.user_story))
        return urwid.Text(description)

    def _milestone_selector(self):
        contents = []
        for milestone in data.list_of_milestones(self.project):
            option = MilestoneOptionEntry(milestone)
            self.options.append(option)

            contents.append(option)
            contents.append(generic.box_solid_fill(" ", 1))

        list_walker = urwid.SimpleFocusListWalker(contents)
        if len(contents) > 0:
            list_walker.set_focus(0)
        return urwid.BoxAdapter(urwid.ListBox(list_walker), 20)

    def _buttons(self):
        self.cancel_button = generic.PlainButton("Cancel")

        colum_items = [("weight", 1, urwid.Text(""))]
        colum_items.append((15, urwid.AttrMap(urwid.Padding(self.cancel_button, right=1, left=2),
                                              "popup-cancel-button")))
        return urwid.Columns(colum_items)


class MilestoneOptionEntry(mixins.KeyPressMixin, urwid.WidgetWrap):
    def __init__(self, milestone):
        self.milestone = milestone

        content = [
            urwid.Columns([
                (3, self._is_closed_widget()),
                ("weight", 0.8, self._name_widget()),
                ("weight", 0.2, self._progress_status_widget()),
            ]),
            urwid.Columns([
                (3, urwid.Text("")),
                ("weight", 0.4, self._finish_date_widget()),
                ("weight", 0.4, self._total_points_widget()),
                ("weight", 0.4, self._closed_points_widget()),
            ])
        ]

        self.widget = urwid.Pile(content)
        super().__init__(urwid.AttrMap(urwid.LineBox(urwid.AttrMap(self.widget, "default")),
                                       "default", "focus"))

    def selectable(self):
        return True

    def _is_closed_widget(self):
        if self.milestone.get("closed", False):
            return urwid.AttrMap(generic.ListText("☑"), "green")
        else:
            return urwid.AttrMap(generic.ListText("☒"), "red")

    def _name_widget(self):
        return urwid.Text(data.milestone_name(self.milestone))

    def _progress_status_widget(self):
        return urwid.ProgressBar("progressbar-normal",
                                 "progressbar-complete",
                                 data.milestone_closed_points(self.milestone),
                                 data.milestone_total_points(self.milestone),
                                 "progressbar-smooth")

    def _finish_date_widget(self):
        return urwid.Columns([
           urwid.Text("Finish date"),
           urwid.Text(("cyan", data.milestone_finish_date(self.milestone))),
        ])

    def _total_points_widget(self):
        return urwid.Columns([
           urwid.Text("Total points"),
           generic.SemaphorePercentText(data.milestone_total_points(self.milestone),
                                        data.milestone_total_points(self.milestone))
        ])

    def _closed_points_widget(self):
         return urwid.Columns([
           urwid.Text("Closed points"),
           generic.SemaphorePercentText(data.milestone_closed_points(self.milestone),
                                        data.milestone_total_points(self.milestone))
        ])
