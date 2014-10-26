from concurrent.futures import Future
from unittest import mock

from taiga_ncurses.ui import signals, views
from taiga_ncurses import controllers
from taiga_ncurses.config import settings
from taiga_ncurses.executor import Executor
from taiga_ncurses.core import StateMachine

from tests import factories


def test_sprints_controller_show_the_help_popup():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.milestone)

    assert not hasattr(project_detail_controller.view.sprint, "help_popup")
    project_detail_controller.handle(settings.data.milestone.keys.help)
    assert hasattr(project_detail_controller.view.sprint, "help_popup")

def test_sprints_controller_close_the_help_popup():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.milestone)
    project_detail_controller.handle(settings.data.milestone.keys.help)

    assert hasattr(project_detail_controller.view.sprint, "help_popup")
    help_popup = project_detail_controller.view.sprint.help_popup
    signals.emit(help_popup.close_button, "click")
    assert not hasattr(project_detail_controller.view.sprint, "help_popup")

def test_sprints_controller_reload():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.milestone)
    executor.milestone.reset_mock()
    executor.milestone_stats.reset_mock()
    executor.user_stories.reset_mock()
    executor.tasks.reset_mock()

    assert executor.milestone.call_count == 0
    assert executor.milestone_stats.call_count == 0
    assert executor.user_stories.call_count == 0
    assert executor.tasks.call_count == 0
    project_detail_controller.handle(settings.data.milestone.keys.reload)
    assert executor.milestone.call_count == 1
    assert executor.milestone_stats.call_count == 1
    assert executor.user_stories.call_count == 1
    assert executor.tasks.call_count == 1

def test_sprint_controller_show_the_new_user_story_form():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.milestone)

    assert not hasattr(project_detail_controller.sprint.view, "user_story_form")
    project_detail_controller.handle(settings.data.milestone.keys.create_user_story)
    assert hasattr(project_detail_controller.sprint.view, "user_story_form")
    assert (project_detail_controller.sprint.view.user_story_form.user_story["milestone"] ==
            project_detail_controller.sprint.view._milestone["id"])

def test_sprint_controller_cancel_the_new_user_story_form():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.milestone)
    project_detail_controller.handle(settings.data.milestone.keys.create_user_story)

    assert hasattr(project_detail_controller.sprint.view, "user_story_form")
    form = project_detail_controller.sprint.view.user_story_form
    signals.emit(form.cancel_button, "click")
    assert not hasattr(project_detail_controller.sprint.view, "user_story_form")

def test_sprint_controller_submit_the_new_user_story_form_with_errors():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.sprint.notifier = mock.Mock()
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.milestone)
    project_detail_controller.handle(settings.data.milestone.keys.create_user_story)
    form = project_detail_controller.sprint.view.user_story_form

    form._subject_edit.set_edit_text("")
    signals.emit(form.save_button, "click")
    assert project_view.sprint.notifier.error_msg.call_count == 1

def test_sprint_controller_submit_new_user_story_form_successfully():
    us_subject = "Create a new user story"
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.sprint.notifier = mock.Mock()
    executor = factories.patched_executor(create_user_story_response=factories.future(
                           factories.successful_create_user_story_response(us_subject)))
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.milestone)
    project_detail_controller.handle(settings.data.milestone.keys.create_user_story)
    form = project_detail_controller.sprint.view.user_story_form
    project_view.sprint.notifier.reset_mock()

    form._subject_edit.set_edit_text(us_subject)

    signals.emit(form.save_button, "click")
    assert project_view.sprint.notifier.info_msg.call_count == 1
    assert executor.create_user_story.call_args.call_list()[0][0][0]["subject"] == us_subject
    assert (executor.create_user_story.call_args.call_list()[0][0][0]["milestone"] ==
            project_detail_controller.sprint.view._milestone["id"])
    assert executor.create_user_story.call_count == 1
    assert executor.create_user_story.return_value.result()["subject"] == us_subject

def test_sprint_controller_show_the_new_task_form():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.milestone)
    project_detail_controller.sprint.view.taskboard.widget.set_focus(1)

    assert not hasattr(project_detail_controller.sprint.view, "task_form")
    project_detail_controller.handle(settings.data.milestone.keys.create_task)
    assert hasattr(project_detail_controller.sprint.view, "task_form")

def test_sprint_controller_cancel_the_new_task_form():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.milestone)
    project_detail_controller.sprint.view.taskboard.widget.set_focus(1)
    project_detail_controller.handle(settings.data.milestone.keys.create_task)

    assert hasattr(project_detail_controller.sprint.view, "task_form")
    form = project_detail_controller.sprint.view.task_form
    signals.emit(form.cancel_button, "click")
    assert not hasattr(project_detail_controller.sprint.view, "task_form")

def test_sprint_controller_submit_the_new_task_form_with_errors():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.sprint.notifier = mock.Mock()
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.milestone)
    project_detail_controller.sprint.view.taskboard.widget.set_focus(1)
    project_detail_controller.handle(settings.data.milestone.keys.create_task)
    form = project_detail_controller.sprint.view.task_form

    form._subject_edit.set_edit_text("")
    signals.emit(form.save_button, "click")
    assert project_view.sprint.notifier.error_msg.call_count == 1

def test_sprint_controller_submit_new_task_form_successfully():
    task_subject = "Create a task"
    task_user_story = 12
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.sprint.notifier = mock.Mock()
    executor = factories.patched_executor(create_task_response=factories.future(
                           factories.successful_create_task_response(task_subject, task_user_story)))
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.milestone)
    project_detail_controller.sprint.view.taskboard.widget.set_focus(1)
    project_detail_controller.handle(settings.data.milestone.keys.create_task)
    form = project_detail_controller.sprint.view.task_form
    project_view.sprint.notifier.reset_mock()

    form._subject_edit.set_edit_text(task_subject)
    form._user_story_combo.get_selected().value = task_user_story

    signals.emit(form.save_button, "click")
    assert project_view.sprint.notifier.info_msg.call_count == 1
    assert executor.create_task.call_args.call_list()[0][0][0]["subject"] == task_subject
    assert (executor.create_task.call_args.call_list()[0][0][0]["milestone"] ==
            project_detail_controller.sprint.view._milestone["id"])
    assert executor.create_task.call_args.call_list()[0][0][0]["user_story"] == task_user_story
    assert executor.create_task.call_count == 1
    assert executor.create_task.return_value.result()["subject"] == task_subject
    assert (executor.create_task.return_value.result()["milestone"] ==
            project_detail_controller.sprint.view._milestone["id"])
    assert executor.create_task.return_value.result()["user_story"] == task_user_story

def test_sprint_controller_show_the_edit_user_story_form():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.milestone)

    assert not hasattr(project_detail_controller.sprint.view, "user_story_form")
    project_detail_controller.handle(settings.data.milestone.keys.edit)
    assert hasattr(project_detail_controller.sprint.view, "user_story_form")
    assert (project_detail_controller.sprint.view.user_story_form.user_story ==
            project_detail_controller.sprint.view.taskboard.widget.get_focus()[0].user_story)

def test_sprint_controller_cancel_the_edit_user_story_form():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.milestone)
    project_detail_controller.handle(settings.data.milestone.keys.edit)

    assert hasattr(project_detail_controller.sprint.view, "user_story_form")
    form = project_detail_controller.sprint.view.user_story_form
    signals.emit(form.cancel_button, "click")
    assert not hasattr(project_detail_controller.sprint.view, "user_story_form")

def test_sprint_controller_submit_the_edit_user_story_form_with_errors():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.sprint.notifier = mock.Mock()
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.milestone)
    project_detail_controller.handle(settings.data.milestone.keys.edit)
    form = project_detail_controller.sprint.view.user_story_form

    form._subject_edit.set_edit_text("")
    signals.emit(form.save_button, "click")
    assert project_view.sprint.notifier.error_msg.call_count == 1

def test_sprint_controller_submit_edit_user_story_form_successfully():
    us_subject = "Update a user story"
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.sprint.notifier = mock.Mock()
    executor = factories.patched_executor(update_user_story_response=factories.future(
                           factories.successful_update_user_story_response(us_subject)))
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.milestone)
    project_detail_controller.handle(settings.data.milestone.keys.edit)
    form = project_detail_controller.sprint.view.user_story_form
    project_view.sprint.notifier.reset_mock()

    form._subject_edit.set_edit_text(us_subject)

    signals.emit(form.save_button, "click")
    assert project_view.sprint.notifier.info_msg.call_count == 1
    assert (executor.update_user_story.call_args.call_list()[0][0][0]["id"] == form.user_story["id"])
    assert executor.update_user_story.call_args.call_list()[0][0][1]["subject"] == us_subject
    assert executor.update_user_story.call_count == 1
    assert executor.update_user_story.return_value.result()["subject"] == us_subject

def test_sprint_controller_show_the_edit_task_form():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.milestone)
    project_detail_controller.sprint.view.taskboard.widget.set_focus(1)

    assert not hasattr(project_detail_controller.sprint.view, "task_form")
    project_detail_controller.handle(settings.data.milestone.keys.edit)
    assert hasattr(project_detail_controller.sprint.view, "task_form")
    assert (project_detail_controller.sprint.view.task_form.task ==
            project_detail_controller.sprint.view.taskboard.widget.get_focus()[0].task)

def test_sprint_controller_cancel_the_edit_task_form():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.milestone)
    project_detail_controller.sprint.view.taskboard.widget.set_focus(1)
    project_detail_controller.handle(settings.data.milestone.keys.edit)

    assert hasattr(project_detail_controller.sprint.view, "task_form")
    form = project_detail_controller.sprint.view.task_form
    signals.emit(form.cancel_button, "click")
    assert not hasattr(project_detail_controller.sprint.view, "task_form")

def test_sprint_controller_submit_the_edit_task_form_with_errors():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.sprint.notifier = mock.Mock()
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.milestone)
    project_detail_controller.sprint.view.taskboard.widget.set_focus(1)
    project_detail_controller.handle(settings.data.milestone.keys.edit)
    form = project_detail_controller.sprint.view.task_form

    form._subject_edit.set_edit_text("")
    signals.emit(form.save_button, "click")
    assert project_view.sprint.notifier.error_msg.call_count == 1

def test_sprint_controller_submit_edit_task_form_successfully():
    task_subject = "Update a task"
    task_user_story = 12
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.sprint.notifier = mock.Mock()
    executor = factories.patched_executor(update_task_response=factories.future(
                           factories.successful_update_task_response(task_subject, task_user_story)))
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.milestone)
    project_detail_controller.sprint.view.taskboard.widget.set_focus(1)
    project_detail_controller.handle(settings.data.milestone.keys.edit)
    form = project_detail_controller.sprint.view.task_form
    project_view.sprint.notifier.reset_mock()

    form._subject_edit.set_edit_text(task_subject)
    form._user_story_combo.get_selected().value = task_user_story

    signals.emit(form.save_button, "click")
    assert project_view.sprint.notifier.info_msg.call_count == 1
    assert (executor.update_task.call_args.call_list()[0][0][0]["id"] == form.task["id"])
    assert executor.update_task.call_args.call_list()[0][0][1]["subject"] == task_subject
    assert (executor.update_task.call_args.call_list()[0][0][1]["milestone"] ==
            project_detail_controller.sprint.view._milestone["id"])
    assert executor.update_task.call_args.call_list()[0][0][1]["user_story"] == task_user_story
    assert executor.update_task.call_count == 1
    assert executor.update_task.return_value.result()["subject"] == task_subject
    assert (executor.update_task.return_value.result()["milestone"] ==
            project_detail_controller.sprint.view._milestone["id"])
    assert executor.update_task.return_value.result()["user_story"] == task_user_story

def test_sprint_controller_delete_user_story_with_errors():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.sprint.notifier = mock.Mock()
    executor = factories.patched_executor(delete_user_story_response=factories.future(None))
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.milestone)

    project_detail_controller.handle(settings.data.milestone.keys.delete)
    assert project_view.sprint.notifier.error_msg.call_count == 1
    assert (executor.delete_user_story.call_args.call_list()[0][0][0]["id"] ==
            project_detail_controller.sprint.view._user_stories[0]["id"])

def test_sprint_controller_delete_user_story_with_success():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.sprint.notifier = mock.Mock()
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.milestone)
    project_view.sprint.notifier.reset_mock()

    project_detail_controller.handle(settings.data.milestone.keys.delete)
    assert project_view.sprint.notifier.info_msg.call_count == 1
    assert (executor.delete_user_story.call_args.call_list()[0][0][0]["id"] ==
            project_detail_controller.sprint.view._user_stories[0]["id"])

def test_sprint_controller_delete_task_with_errors():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.sprint.notifier = mock.Mock()
    executor = factories.patched_executor(delete_task_response=factories.future(None))
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.milestone)

    project_view.sprint.taskboard.list_walker.set_focus(2)
    project_detail_controller.handle(settings.data.milestone.keys.delete)
    assert project_view.sprint.notifier.error_msg.call_count == 1
    assert (executor.delete_task.call_args.call_list()[0][0][0]["id"] ==
            project_detail_controller.sprint.view._tasks[1]["id"])

def test_sprint_controller_delete_task_with_success():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.sprint.notifier = mock.Mock()
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.milestone)
    project_view.sprint.notifier.reset_mock()

    project_view.sprint.taskboard.list_walker.set_focus(2)
    project_detail_controller.handle(settings.data.milestone.keys.delete)
    assert project_view.sprint.notifier.info_msg.call_count == 1
    assert (executor.delete_task.call_args.call_list()[0][0][0]["id"] ==
            project_detail_controller.sprint.view._tasks[1]["id"])

def test_sprint_controller_show_the_milestone_selector_popup():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.milestone)

    assert not hasattr(project_detail_controller.view.sprint, "milestone_selector_popup")
    project_detail_controller.handle(settings.data.milestone.keys.change_to_milestone)
    assert hasattr(project_detail_controller.view.sprint, "milestone_selector_popup")

def test_sprint_controller_close_the_milestone_selector_popup():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.milestone)
    project_detail_controller.handle(settings.data.milestone.keys.change_to_milestone)

    assert hasattr(project_detail_controller.view.sprint, "milestone_selector_popup")
    milestone_selector_popup = project_detail_controller.view.sprint.milestone_selector_popup
    signals.emit(milestone_selector_popup.cancel_button, "click")
    assert not hasattr(project_detail_controller.view.sprint, "milestone_selector_popup")

def test_sprint_controller_change_to_another_milestone():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.sprint.notifier = mock.Mock()
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.milestone)
    project_detail_controller.handle(settings.data.milestone.keys.change_to_milestone)
    milestone_selector_popup = project_detail_controller.view.sprint.milestone_selector_popup
    project_view.sprint.notifier.reset_mock()
    executor.milestone.reset_mock()
    executor.milestone_stats.reset_mock()
    executor.user_stories.reset_mock()
    executor.tasks.reset_mock()

    assert project_view.sprint.notifier.info_msg.call_count == 0
    assert executor.milestone.call_count == 0
    assert executor.milestone_stats.call_count == 0
    assert executor.user_stories.call_count == 0
    assert executor.tasks.call_count == 0
    signals.emit(milestone_selector_popup.options[2], "click")
    assert project_view.sprint.notifier.info_msg.call_count == 1
    assert executor.milestone.call_count == 1
    assert executor.milestone_stats.call_count == 1
    assert executor.user_stories.call_count == 1
    assert executor.tasks.call_count == 1
    assert (project_detail_controller.sprint.view._milestone["id"] ==
            milestone_selector_popup.project["list_of_milestones"][-1]["id"])

def test_sprint_controller_change_user_story_status():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.sprint.notifier = mock.Mock()
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.milestone)
    project_view.sprint.notifier.reset_mock()

    us = project_view.sprint.taskboard.widget.contents()[0][0]
    combo = us.base_widget.widget.contents[2][0]    # 2 => status
    item = combo.menu.get_item(0)                   # 0 => New
    combo.item_changed(item, True)

    assert project_view.sprint.notifier.info_msg.call_count == 1
    assert executor.update_user_story.call_args.call_list()[0][0][1]["status"] == item.value
    assert executor.update_user_story.call_count == 1

def test_sprint_controller_change_user_story_points():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.sprint.notifier = mock.Mock()
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.milestone)
    project_view.sprint.notifier.reset_mock()

    us = project_view.sprint.taskboard.widget.contents()[0][0]
    combo = us.base_widget.widget.contents[3][0].contents[1][0]     # 3 => points
    item = combo.menu.get_item(2)                                   # 2 => 1/2
    combo.item_changed(item, True)

    assert project_view.sprint.notifier.info_msg.call_count == 1
    assert list(executor.update_user_story.call_args.call_list()[0][0][1]["points"].values())[0] == item.value
    assert executor.update_user_story.call_count == 1

def test_sprint_controller_change_task_status():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.sprint.notifier = mock.Mock()
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.milestone)
    project_view.sprint.notifier.reset_mock()

    task = project_view.sprint.taskboard.widget.contents()[1][0]
    combo = task.base_widget.widget.contents[3][0]      # 3 => status
    item = combo.menu.get_item(0)                       # 0 => New
    combo.item_changed(item, True)

    assert project_view.sprint.notifier.info_msg.call_count == 1
    assert executor.update_task.call_args.call_list()[0][0][1]["status"] == item.value
    assert executor.update_task.call_count == 1

def test_sprint_controller_change_task_assigned_to():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.sprint.notifier = mock.Mock()
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.milestone)
    project_view.sprint.notifier.reset_mock()

    task = project_view.sprint.taskboard.widget.contents()[1][0]
    combo = task.base_widget.widget.contents[2][0]      # 2 => assigned_to
    item = combo.menu.get_item(0)                       # 0
    combo.item_changed(item, True)

    assert project_view.sprint.notifier.info_msg.call_count == 1
    assert executor.update_task.call_args.call_list()[0][0][1]["assigned_to"] == item.value
    assert executor.update_task.call_count == 1
