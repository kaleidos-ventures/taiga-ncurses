# -*- coding: utf-8 -*-

"""
taiga_ncurses.ui.widgets.milestones
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import urwid

from taiga_ncurses import data

from . import generic, mixins, utils


class MilestoneInfo(urwid.WidgetWrap):
    def __init__(self, project):
        self.project = project
        self.widget = urwid.Columns([])
        super().__init__(self.widget)

    def populate(self, milestone):
        self._w = urwid.Columns([
            ("weight", 1, generic.ListText(data.milestone_name(milestone))),
        ])


class MilestoneStats(urwid.WidgetWrap):
    def __init__(self, project):
        self.project = project
        self.widget = urwid.Columns([])
        super().__init__(self.widget)

    def populate(self, milestone_stats):
        self._w = urwid.Columns([
            ("weight", 0.2, urwid.LineBox(MilestoneStatsStatus(milestone_stats), "Status")),
            ("weight", 0.3, urwid.LineBox(MilestoneStatsPoints(milestone_stats), "Points")),
            ("weight", 0.3, urwid.LineBox(MilestoneStatsTasks(milestone_stats), "Tasks")),
            ("weight", 0.3, urwid.LineBox(MilestoneStatsDates(milestone_stats), "Dates")),
         ])


class MilestoneStatsStatus(urwid.Pile):
    def __init__(self, milestone_stats):
        items = [generic.box_solid_fill(" ", 1)]
        items.append(urwid.ProgressBar("progressbar-normal",
                                       "progressbar-complete",
                                       data.milestone_completed_points(milestone_stats),
                                       data.milestone_total_points(milestone_stats),
                                       "progressbar-smooth"))
        super().__init__(items)


class MilestoneStatsPoints(urwid.Pile):
    def __init__(self, milestone_stats):
        total = data.milestone_total_points(milestone_stats)
        completed = data.milestone_completed_points(milestone_stats)
        remaining = total - completed

        items = [
            urwid.Pile([generic.ListText("Total"), generic.SemaphorePercentText(total, max_value=total)]),
            urwid.Pile([generic.ListText("Completed"), generic.SemaphorePercentText(completed, max_value=total)]),
            urwid.Pile([generic.ListText("Remaining"), generic.SemaphorePercentText(remaining, max_value=total,
                                                                                    invert=True)])
        ]
        super().__init__([urwid.Columns(items)])


class MilestoneStatsTasks(urwid.Pile):
    def __init__(self, milestone_stats):
        total = data.milestone_total_tasks(milestone_stats)
        completed = data.milestone_completed_tasks(milestone_stats)
        remaining = total - completed

        items = [
            urwid.Pile([generic.ListText("Total"), generic.SemaphorePercentText(total, max_value=total)]),
            urwid.Pile([generic.ListText("Completed"), generic.SemaphorePercentText(completed, max_value=total)]),
            urwid.Pile([generic.ListText("Remaining"), generic.SemaphorePercentText(remaining, max_value=total,
                                                                                    invert=True)])
        ]
        super().__init__([urwid.Columns(items)])


class MilestoneStatsDates(urwid.Pile):
    def __init__(self, milestone_stats):
        items = [
            urwid.Pile([generic.ListText("Start"), generic.ListText(("cyan", data.milestone_estimated_start(
                                                                                             milestone_stats)))]),
            urwid.Pile([generic.ListText("Finish"), generic.ListText(("cyan", data.milestone_estimated_finish(
                                                                                               milestone_stats)))])
        ]
        remaining_days = data.milestone_remaining_days(milestone_stats)
        if remaining_days > 1 :
            items.append(urwid.Pile([generic.ListText("Remaining"), generic.ListText(
                                          ("green", "{} days".format(remaining_days)))]))
        elif remaining_days == 1:
            items.append(urwid.Pile([generic.ListText("Remaining"), generic.ListText(
                                           ("green", "{} day".format(remaining_days)))]))
        else:
            items.append(urwid.Pile([generic.ListText("Remaining"), generic.ListText(
                                                                    ("red", "0 days"))]))

        super().__init__([urwid.Columns(items)])


class MilestoneTaskboard(urwid.WidgetWrap):
    on_task_status_change = None
    on_task_assigned_to_change = None
    on_user_story_status_change = None
    on_user_story_points_change = None

    def __init__(self, project):
        self.project = project
        self.roles = data.computable_roles(project)

        self.list_walker = urwid.SimpleFocusListWalker([
            generic.ListText("No items in this Milestone"),
        ])
        self.widget = urwid.ListBox(self.list_walker)
        super().__init__(self.widget)

    def populate(self, user_stories, tasks):
        if user_stories:
            self.reset()

        # Task with user stories
        for us in user_stories:
            self.list_walker.append(UserStoryEntry(us, self.project, self.roles,
                                                  self.on_user_story_status_change,
                                                  self.on_user_story_points_change))
            for task in data.tasks_per_user_story(tasks, us):
                self.list_walker.append(TaskEntry(task, self.project, self.on_task_status_change,
                                              self.on_task_assigned_to_change))

        # Unasigned task
        self.list_walker.append(UnasignedTasksHeaderEntry())
        for task in data.unassigned_tasks(tasks):
            self.list_walker.append(TaskEntry(task, self.project, self.on_task_status_change,
                                              self.on_task_assigned_to_change))

        if len(self.list_walker) > 0:
            self.list_walker.set_focus(0)

    def reset(self):
        self.list_walker.clear()


class UserStoryEntry(urwid.WidgetWrap):
    def __init__(self, us, project, roles, on_status_change=None, on_points_change=None):
        self.user_story = us

        if us.get("is_closed", False):
            is_closed = urwid.AttrMap(generic.ListText("☑"), "green", "focus-header")
        else:
            is_closed = urwid.AttrMap(generic.ListText("☒"), "red", "focus-header")
        colum_items = [("weight", 0.05, is_closed)]

        us_ref_and_name = "US #{0: <4} {1}".format(str(data.us_ref(us)), data.us_subject(us))
        colum_items.append(("weight", 0.6, generic.ListText(us_ref_and_name, align="left")))

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
            role_name = generic.ListText("{}:".format(role.get("name", "UNK.")))

            selected = (us.get("points", {}).get(r_id, None) or
                        project.get("default_points", None))
            points_combo = generic.ComboBox(items, selected_value=selected, style="cyan",
                                            on_state_change=on_points_change, user_data=(us, r_id))
            colum_items.append(("weight", 0.15, urwid.Columns([('pack',role_name), points_combo])))

        colum_items.append(("weight", 0.1, generic.ListText(("green", "TOTAL: {0:.1f}".format(
                                                                      data.us_total_points(us))))))

        self.widget = urwid.Columns(colum_items)
        super().__init__(urwid.AttrMap(urwid.LineBox(urwid.AttrMap(self.widget, "cyan", "focus-header")),
                                       "green"))

    def selectable(self):
        return True


class UnasignedTasksHeaderEntry(urwid.WidgetWrap):
    def __init__(self):
        self.widget = urwid.Columns([generic.ListText("Unassigned tasks")])
        super().__init__(urwid.AttrMap(urwid.LineBox(urwid.AttrMap(self.widget, "cyan", "focus-header")),
                                       "green"))

    def selectable(self):
        return True


class TaskEntry(urwid.WidgetWrap):
    def __init__(self, task, project, on_status_change=None, on_assigned_to_change=None):
        self.task = task

        if data.task_finished_date(task):
            is_closed = urwid.AttrMap(generic.ListText("☑"), "green", "focus")
        else:
            is_closed = urwid.AttrMap(generic.ListText("☒"), "red", "focus")
        colum_items = [("weight", 0.05, is_closed)]

        task_ref_and_subject = "Task #{0: <4} {1}".format(data.task_ref(task), data.task_subject(task))
        if task.get("is_iocaine", False):
            task_ref_and_subject = [task_ref_and_subject + " ", (("magenta"), "☣")]
        colum_items.append(("weight", 1, generic.ListText(task_ref_and_subject, align="left")))

        memberships = [{"user": None, "full_name": "Unassigned"}] + list(data.active_memberships(project).values())
        items = tuple(((urwid.AttrSpec("h{0}".format(utils.color_to_hex(s.get("color", "#ffffff"))), "default"),
                        s.get("full_name", "")), s.get("user", None)) for s in memberships)
        selected = task.get("assigned_to", None)
        assigned_to_combo = generic.ComboBox(items, selected_value=selected, style="cyan", enable_markup=True,
                                             on_state_change=on_assigned_to_change, user_data=task)
        colum_items.append(("weight", 0.2, assigned_to_combo))

        task_statuses = data.task_statuses(project)
        items = tuple(((urwid.AttrSpec("h{0}".format(utils.color_to_hex(s.get("color", "#ffffff"))), "default"),
                        s.get("name", "")), s.get("id", None)) for s in task_statuses.values())
        selected = task.get("status", None) or project.get("default_task_status", None)
        status_combo = generic.ComboBox(items, selected_value=selected, style="cyan", enable_markup=True,
                                        on_state_change=on_status_change, user_data=task)
        colum_items.append(("weight", 0.2, status_combo))

        self.widget = urwid.Columns(colum_items)
        super().__init__(urwid.AttrMap(self.widget, "default", "focus"))

    def selectable(self):
        return True


class MIlestoneSelectorPopup(mixins.FormMixin, urwid.WidgetWrap):
    def __init__(self, project, current_milestone={}):
        self.project = project
        self.current_milestone = current_milestone
        self.options = []

        contents = [
            generic.box_solid_fill(" ", 2),
            urwid.Padding(self._milestone_selector(), right=2, left=2),
            generic.box_solid_fill(" ", 2),
            self._buttons(),
            generic.box_solid_fill(" ", 1),
        ]
        self.widget = urwid.Pile(contents)

        title = "Change to another Milestone"
        super().__init__(urwid.AttrMap(urwid.LineBox(urwid.Padding(self.widget, right=2, left=2),
                                                     title), "popup"))

    def _milestone_selector(self):
        contents = []
        for milestone in data.list_of_milestones(self.project):
            option = MilestoneOptionEntry(milestone, not data.milestones_are_equals(self.current_milestone,
                                                                               milestone))
            if option.selectable():
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
    is_selectable = True

    def __init__(self, milestone, is_selectable=True):
        self.milestone = milestone
        self.is_selectable = is_selectable

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
                                       "default" if self.is_selectable else "popup-selected", "focus"))

    def selectable(self):
        return self.is_selectable

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

class TaskForm(mixins.FormMixin, urwid.WidgetWrap):
    _user_story_combo = None
    _status_combo = None
    _assigned_to_combo = None

    def __init__(self, project, user_stories, task={}):
        self.project = project
        self.user_stories = user_stories
        self.task = task

        contents = [
            generic.box_solid_fill(" ", 2),
            self._form_inputs(),
            generic.box_solid_fill(" ", 2),
            self._buttons(),
            generic.box_solid_fill(" ", 1),
        ]
        self.widget = urwid.Pile(contents)

        title = "Edit Task" if self.user_story else "Create Task"
        super().__init__(urwid.AttrMap(urwid.LineBox(urwid.Padding(self.widget, right=2, left=2),
                                                     title), "popup"))

    @property
    def subject(self):
        return self._subject_edit.get_edit_text()

    @property
    def user_story(self):
        return self._user_story_combo.get_selected().value

    @property
    def status(self):
        return self._status_combo.get_selected().value

    @property
    def assigned_to(self):
        return self._assigned_to_combo.get_selected().value

    @property
    def is_iocaine(self):
        return self._is_iocaine_checkbox.get_state()

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
            self._user_story_input(),
            generic.box_solid_fill(" ", 1),
            self._status_input(),
            generic.box_solid_fill(" ", 1),
            self._assigned_to_input(),
            generic.box_solid_fill(" ", 1),
            self._is_iocaine_input(),
            generic.box_solid_fill(" ", 1),
            self._tags_input(),
            generic.box_solid_fill(" ", 1),
            self._description_input(),
        ]

        list_walker = urwid.SimpleFocusListWalker(contents)
        list_walker.set_focus(0)
        return urwid.BoxAdapter(urwid.ListBox(list_walker), 13)

    def _subject_input(self):
        self._subject_edit = urwid.Edit(edit_text=self.task.get("subject", ""))

        colum_items = [(17, urwid.Padding(generic.ListText("Subject", align="right"), right=4))]
        colum_items.append(urwid.AttrMap(self._subject_edit, "popup-editor"))
        return urwid.Columns(colum_items)

    def _user_story_input(self):
        uss = [{"id": None, "subject": "None"}] + self.user_stories
        items = tuple(("US #{} - {}".format(u.get("ref", "**"),
                                            u.get("subject", "-no name-")) if u.get("id", None) else
                           u.get("subject", "- no name -"),
                       u.get("id", None)) for u in uss)
        selected = self.task.get("user_story", None)

        self._user_story_combo = generic.ComboBox(items, selected_value=selected, style="cyan")

        colum_items = [(17, urwid.Padding(generic.ListText("User story", align="right"), right=4))]
        colum_items.append(self._user_story_combo)
        return urwid.Columns(colum_items)

    def _status_input(self):
        task_statuses = data.task_statuses(self.project)
        items = tuple(((urwid.AttrSpec("h{0}".format(utils.color_to_hex(s.get("color", "#ffffff"))), "default"),
                        s.get("name", "")), s.get("id", None)) for s in task_statuses.values())
        selected = self.task.get("status", None) or self.project.get("default_task_status", None)

        self._status_combo = generic.ComboBox(items, selected_value=selected, style="cyan")

        colum_items = [(17, urwid.Padding(generic.ListText("Status", align="right"), right=4))]
        colum_items.append(self._status_combo)
        return urwid.Columns(colum_items)

    def _assigned_to_input(self):
        memberships = [{"user": None, "full_name": "Unassigned"}] + list(data.active_memberships(self.project).values())
        items = tuple(((urwid.AttrSpec("h{0}".format(utils.color_to_hex(s.get("color", "#ffffff"))), "default"),
                        s.get("full_name", "")), s.get("user", None)) for s in memberships)
        selected = self.task.get("assigned_to", None)

        self._assigned_to_combo = generic.ComboBox(items, selected_value=selected, style="cyan")

        colum_items = [(17, urwid.Padding(generic.ListText("Assigned to", align="right"), right=4))]
        colum_items.append(self._assigned_to_combo)
        return urwid.Columns(colum_items)

    def _is_iocaine_input(self):
        self._is_iocaine_checkbox = urwid.CheckBox(["Is iocaine ", (("popup-text-magenta"), "☣")],
                state=self.task.get("is_iocaine", False))

        colum_items = [(17, urwid.Text(" "))]
        colum_items.append(self._is_iocaine_checkbox)
        return urwid.Columns(colum_items)

    def _tags_input(self):
        self._tags_edit = urwid.Edit(edit_text=", ".join(self.task.get("tags", [])))

        colum_items = [(17, urwid.Padding(generic.ListText("Tags", align="right"), right=4))]
        colum_items.append(urwid.AttrMap(self._tags_edit, "popup-editor"))
        return urwid.Columns(colum_items)

    def _description_input(self):
        self._description_edit = urwid.Edit(multiline=True, edit_text=self.task.get("description", ""))

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
