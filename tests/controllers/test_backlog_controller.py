from concurrent.futures import Future
from unittest import mock

from taiga_ncurses.ui import signals, views
from taiga_ncurses import controllers
from taiga_ncurses.config import settings
from taiga_ncurses.executor import Executor
from taiga_ncurses.core import StateMachine

from tests import factories


def test_backlog_controller_show_the_help_popup():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)

    assert not hasattr(project_detail_controller.view.backlog, "help_popup")
    project_detail_controller.handle(settings.data.backlog.keys.help)
    assert hasattr(project_detail_controller.view.backlog, "help_popup")

def test_backlog_controller_close_the_help_popup():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.backlog.keys.help)

    assert hasattr(project_detail_controller.view.backlog, "help_popup")
    help_popup = project_detail_controller.view.backlog.help_popup
    signals.emit(help_popup.close_button, "click")
    assert not hasattr(project_detail_controller.view.backlog, "help_popup")

def test_backlog_controller_reload():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    executor.project_stats.reset_mock()
    executor.unassigned_user_stories.reset_mock()

    assert executor.project_stats.call_count == 0
    assert executor.unassigned_user_stories.call_count == 0
    project_detail_controller.handle(settings.data.backlog.keys.reload)
    assert executor.project_stats.call_count == 1
    assert executor.unassigned_user_stories.call_count == 1

def test_backlog_controller_show_the_new_user_story_form():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)

    assert not hasattr(project_detail_controller.view.backlog, "user_story_form")
    project_detail_controller.handle(settings.data.backlog.keys.create)
    assert hasattr(project_detail_controller.view.backlog, "user_story_form")

def test_backlog_controller_cancel_the_new_user_story_form():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.backlog.keys.create)

    assert hasattr(project_detail_controller.view.backlog, "user_story_form")
    form = project_detail_controller.view.backlog.user_story_form
    signals.emit(form.cancel_button, "click")
    assert not hasattr(project_detail_controller.view.backlog, "user_story_form")

def test_backlog_controller_submit_new_user_story_form_with_errors():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.backlog.notifier = mock.Mock()
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.backlog.keys.create)
    form = project_detail_controller.view.backlog.user_story_form

    signals.emit(form.save_button, "click")
    assert project_view.backlog.notifier.error_msg.call_count == 1

def test_backlog_controller_submit_new_user_story_form_successfully():
    us_subject = "Create a new user story"
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.backlog.notifier = mock.Mock()
    executor = factories.patched_executor(create_user_story_response=factories.future(
                           factories.successful_create_user_story_response(us_subject)))
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.backlog.keys.create)
    form = project_detail_controller.view.backlog.user_story_form
    project_view.backlog.notifier.reset_mock()

    form._subject_edit.set_edit_text(us_subject)
    signals.emit(form.save_button, "click")
    assert project_view.backlog.notifier.info_msg.call_count == 1
    assert executor.create_user_story.call_args.call_list()[0][0][0]["subject"] == us_subject
    assert executor.create_user_story.call_count == 1
    assert executor.create_user_story.return_value.result()["subject"] == us_subject

def test_backlog_controller_show_the_edit_user_story_form():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)

    assert not hasattr(project_detail_controller.view.backlog, "user_story_form")
    project_detail_controller.handle(settings.data.backlog.keys.edit)
    assert hasattr(project_detail_controller.view.backlog, "user_story_form")
    assert (project_detail_controller.view.backlog.user_story_form.user_story ==
            project_detail_controller.view.backlog.user_stories.widget.get_focus().user_story)

def test_backlog_controller_cancel_the_edit_user_story_form():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.backlog.keys.edit)

    assert hasattr(project_detail_controller.view.backlog, "user_story_form")
    form = project_detail_controller.view.backlog.user_story_form
    signals.emit(form.cancel_button, "click")
    assert not hasattr(project_detail_controller.view.backlog, "user_story_form")

def test_backlog_controller_submit_the_edit_user_story_form_with_errors():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.backlog.notifier = mock.Mock()
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.backlog.keys.edit)
    form = project_detail_controller.view.backlog.user_story_form

    form._subject_edit.set_edit_text("")
    signals.emit(form.save_button, "click")
    assert project_view.backlog.notifier.error_msg.call_count == 1

def test_backlog_controller_submit_edit_user_story_form_successfully():
    us_subject = "Update a user story"
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.backlog.notifier = mock.Mock()
    executor = factories.patched_executor(update_user_story_response=factories.future(
                           factories.successful_update_user_story_response(us_subject)))
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.backlog.keys.edit)
    form = project_detail_controller.view.backlog.user_story_form
    project_view.backlog.notifier.reset_mock()

    form._subject_edit.set_edit_text(us_subject)

    signals.emit(form.save_button, "click")
    assert project_view.backlog.notifier.info_msg.call_count == 1
    assert (executor.update_user_story.call_args.call_list()[0][0][0]["id"] == form.user_story["id"])
    assert executor.update_user_story.call_args.call_list()[0][0][1]["subject"] == us_subject
    assert executor.update_user_story.call_count == 1
    assert executor.update_user_story.return_value.result()["subject"] == us_subject

def test_backlog_controller_move_user_story_down():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.backlog.notifier = mock.Mock()
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_view.backlog.notifier.reset_mock()

    us_a_old = project_detail_controller.backlog.user_stories[0]
    us_b_old = project_detail_controller.backlog.user_stories[1]

    project_detail_controller.handle(settings.data.backlog.keys.decrease_priority)
    assert project_view.backlog.notifier.info_msg.call_count == 1

    us_b_new = project_detail_controller.backlog.user_stories[0]
    us_a_new = project_detail_controller.backlog.user_stories[1]

    assert us_a_old == us_a_new
    assert us_b_old == us_b_new

def test_backlog_controller_move_user_story_up():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.backlog.notifier = mock.Mock()
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.view.backlog.user_stories.widget.contents.focus = 2
    project_view.backlog.notifier.reset_mock()

    us_a_old = project_detail_controller.backlog.user_stories[0]
    us_b_old = project_detail_controller.backlog.user_stories[1]

    project_detail_controller.handle(settings.data.backlog.keys.increase_priority)
    assert project_view.backlog.notifier.info_msg.call_count == 1

    us_b_new = project_detail_controller.backlog.user_stories[0]
    us_a_new = project_detail_controller.backlog.user_stories[1]

    assert us_a_old == us_a_new
    assert us_b_old == us_b_new

def test_backlog_controller_update_user_stories_order_with_errors():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.backlog.notifier = mock.Mock()
    executor = factories.patched_executor(update_user_stories_order_response=factories.future(None))
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)

    project_detail_controller.handle(settings.data.backlog.keys.update_order)
    assert project_view.backlog.notifier.error_msg.call_count == 1

def test_backlog_controller_update_user_stories_order_with_success():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.backlog.notifier = mock.Mock()
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_view.backlog.notifier.reset_mock()

    project_detail_controller.handle(settings.data.backlog.keys.update_order)
    assert project_view.backlog.notifier.info_msg.call_count == 1

def test_backlog_controller_delete_user_story_with_errors():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.backlog.notifier = mock.Mock()
    executor = factories.patched_executor(delete_user_story_response=factories.future(None))
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)

    project_detail_controller.handle(settings.data.backlog.keys.delete)
    assert project_view.backlog.notifier.error_msg.call_count == 1
    assert (executor.delete_user_story.call_args.call_list()[0][0][0]["id"] ==
            project_detail_controller.backlog.user_stories[0]["id"])

def test_backlog_controller_delete_user_story_with_success():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.backlog.notifier = mock.Mock()
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_view.backlog.notifier.reset_mock()

    project_detail_controller.handle(settings.data.backlog.keys.delete)
    assert project_view.backlog.notifier.info_msg.call_count == 1
    assert (executor.delete_user_story.call_args.call_list()[0][0][0]["id"] ==
            project_detail_controller.backlog.user_stories[0]["id"])

def test_backlog_controller_show_the_milestone_selector_popup():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)

    assert not hasattr(project_detail_controller.view.backlog, "milestone_selector_popup")
    project_detail_controller.handle(settings.data.backlog.keys.move_to_milestone)
    assert hasattr(project_detail_controller.view.backlog, "milestone_selector_popup")

def test_backlog_controller_close_the_milestone_selector_popup():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.backlog.keys.move_to_milestone)

    assert hasattr(project_detail_controller.view.backlog, "milestone_selector_popup")
    milestone_selector_popup = project_detail_controller.view.backlog.milestone_selector_popup
    signals.emit(milestone_selector_popup.cancel_button, "click")
    assert not hasattr(project_detail_controller.view.backlog, "milestone_selector_popup")

def test_backlog_controller_move_a_user_story_to_a_milestone():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.backlog.notifier = mock.Mock()
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.backlog.keys.move_to_milestone)
    milestone_selector_popup = project_detail_controller.view.backlog.milestone_selector_popup
    project_view.backlog.notifier.reset_mock()

    assert project_view.backlog.notifier.info_msg.call_count == 0
    assert executor.update_user_story.call_count == 0
    signals.emit(milestone_selector_popup.options[2], "click")
    assert project_view.backlog.notifier.info_msg.call_count == 1
    assert executor.update_user_story.call_count == 1
    assert (executor.update_user_story.call_args.call_list()[0][0][1]["milestone"] ==
            milestone_selector_popup.project["list_of_milestones"][-3]["id"])

def test_backlog_controller_change_user_story_status():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.backlog.notifier = mock.Mock()
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.backlog.keys.edit)
    project_view.backlog.notifier.reset_mock()

    us = project_detail_controller.view.backlog.user_stories.widget.contents[1][0]
    combo = us.base_widget.widget.contents[5][0]    # 5 => status
    item = combo.menu.get_item(0)                   # 0 => New
    combo.item_changed(item, True)

    assert project_view.backlog.notifier.info_msg.call_count == 1
    assert executor.update_user_story.call_args.call_list()[0][0][1]["status"] == item.value
    assert executor.update_user_story.call_count == 1

def test_backlog_controller_change_user_story_points():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.backlog.notifier = mock.Mock()
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.backlog.keys.edit)
    project_view.backlog.notifier.reset_mock()

    us = project_detail_controller.view.backlog.user_stories.widget.contents[1][0]
    combo = us.base_widget.widget.contents[6][0]    # 6 => points
    item = combo.menu.get_item(2)                   # 2 => 1/2
    combo.item_changed(item, True)

    assert project_view.backlog.notifier.info_msg.call_count == 1
    assert list(executor.update_user_story.call_args.call_list()[0][0][1]["points"].values())[0] == item.value
    assert executor.update_user_story.call_count == 1

# BULK

def test_backlog_controller_show_the_new_user_stories_in_bulk_form():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)

    assert not hasattr(project_detail_controller.view.backlog, "user_stories_in_bulk_form")
    project_detail_controller.handle(settings.data.backlog.keys.create_in_bulk)
    assert hasattr(project_detail_controller.view.backlog, "user_stories_in_bulk_form")

def test_backlog_controller_cancel_the_new_user_stories_in_bulk_form():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.backlog.keys.create_in_bulk)

    assert hasattr(project_detail_controller.view.backlog, "user_stories_in_bulk_form")
    form = project_detail_controller.view.backlog.user_stories_in_bulk_form
    signals.emit(form.cancel_button, "click")
    assert not hasattr(project_detail_controller.view.backlog, "user_stories_in_bulk_form")

def test_backlog_controller_submit_new_user_stories_in_bulk_form_with_errors():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.backlog.notifier = mock.Mock()
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.backlog.keys.create_in_bulk)
    form = project_detail_controller.view.backlog.user_stories_in_bulk_form

    signals.emit(form.save_button, "click")
    assert project_view.backlog.notifier.error_msg.call_count == 1

def test_backlog_controller_submit_new_user_stories_in_bulk_form_successfully():
    us_subjects = "Create a new user story 1\nCreate a new user story 2"
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.backlog.notifier = mock.Mock()
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.backlog.keys.create_in_bulk)
    form = project_detail_controller.view.backlog.user_stories_in_bulk_form
    project_view.backlog.notifier.reset_mock()

    form._subjects_edit.set_edit_text(us_subjects)
    signals.emit(form.save_button, "click")
    assert project_view.backlog.notifier.info_msg.call_count == 1
    assert executor.create_user_stories_in_bulk.call_args.call_list()[0][0][0]["bulkStories"] == us_subjects
    assert executor.create_user_stories_in_bulk.call_count == 1
    assert executor.create_user_stories_in_bulk.return_value.result()
