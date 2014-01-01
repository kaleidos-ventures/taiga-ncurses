from concurrent.futures import Future
from unittest import mock

from gmncurses.ui import signals, views
from gmncurses import controllers, config
from gmncurses.executor import Executor
from gmncurses.core import StateMachine

from tests import factories


def test_project_detail_backlog_controller_show_the_help_popup():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)

    assert not hasattr(project_detail_controller.view.backlog, "help_popup")
    project_detail_controller.handle(config.ProjectBacklogKeys.HELP)
    assert hasattr(project_detail_controller.view.backlog, "help_popup")

def test_project_detail_backlog_controller_show_the_new_user_story_form():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)

    assert not hasattr(project_detail_controller.view.backlog, "user_story_form")
    project_detail_controller.handle(config.ProjectBacklogKeys.CREATE_USER_STORY)
    assert hasattr(project_detail_controller.view.backlog, "user_story_form")

def test_project_detail_backlog_controller_submit_new_user_story_form_with_errors():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.backlog.notifier = mock.Mock()
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(config.ProjectBacklogKeys.CREATE_USER_STORY)
    form = project_detail_controller.view.backlog.user_story_form

    signals.emit(form.save_button, "click")
    assert project_view.backlog.notifier.error_msg.call_count == 1

def test_project_detail_backlog_controller_submit_new_user_story_form_successfully():
    us_subject = "Create a new user story"
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.backlog.notifier = mock.Mock()
    executor = factories.patched_executor(create_user_story_response=factories.future(
                           factories.successful_create_user_story_response(us_subject)))
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(config.ProjectBacklogKeys.CREATE_USER_STORY)
    form = project_detail_controller.view.backlog.user_story_form
    project_view.backlog.notifier.reset_mock()

    form._subject_edit.set_edit_text(us_subject)
    signals.emit(form.save_button, "click")
    assert project_view.backlog.notifier.info_msg.call_count == 1
    assert executor.create_user_story.call_args.call_list()[0][0][0]["subject"] == us_subject
    assert executor.create_user_story.call_count == 1
    assert executor.create_user_story.return_value.result()["subject"] == us_subject

def test_project_detail_backlog_controller_show_the_edit_user_story_form():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)

    assert not hasattr(project_detail_controller.view.backlog, "user_story_form")
    project_detail_controller.handle(config.ProjectBacklogKeys.EDIT_USER_STORY)
    assert hasattr(project_detail_controller.view.backlog, "user_story_form")
    assert (project_detail_controller.view.backlog.user_story_form.user_story ==
            project_detail_controller.view.backlog.user_stories.widget.get_focus().user_story)

def test_project_detail_backlog_controller_submit_the_edit_user_story_form_with_errors():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.backlog.notifier = mock.Mock()
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(config.ProjectBacklogKeys.EDIT_USER_STORY)
    form = project_detail_controller.view.backlog.user_story_form

    form._subject_edit.set_edit_text("")
    signals.emit(form.save_button, "click")
    assert project_view.backlog.notifier.error_msg.call_count == 1

def test_project_detail_backlog_controller_submit_edit_user_story_form_successfully():
    us_subject = "Update a user story"
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.backlog.notifier = mock.Mock()
    executor = factories.patched_executor(update_user_story_response=factories.future(
                           factories.successful_update_user_story_response(us_subject)))
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(config.ProjectBacklogKeys.EDIT_USER_STORY)
    form = project_detail_controller.view.backlog.user_story_form
    project_view.backlog.notifier.reset_mock()

    form._subject_edit.set_edit_text(us_subject)
    signals.emit(form.save_button, "click")
    assert project_view.backlog.notifier.info_msg.call_count == 1
    assert (executor.update_user_story.call_args.call_list()[0][0][0]["id"] ==
            project_detail_controller.view.backlog.user_story_form.user_story["id"])
    assert executor.update_user_story.call_args.call_list()[0][0][1]["subject"] == us_subject
    assert executor.update_user_story.call_count == 1
    assert executor.update_user_story.return_value.result()["subject"] == us_subject

def test_project_detail_backlog_controller_move_user_story_down():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.backlog.notifier = mock.Mock()
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_view.backlog.notifier.reset_mock()

    us_a_old = project_detail_controller.backlog.user_stories[0]
    us_b_old = project_detail_controller.backlog.user_stories[1]

    project_detail_controller.handle(config.ProjectBacklogKeys.US_DOWN)
    assert project_view.backlog.notifier.info_msg.call_count == 1

    us_b_new = project_detail_controller.backlog.user_stories[0]
    us_a_new = project_detail_controller.backlog.user_stories[1]

    assert us_a_old == us_a_new
    assert us_b_old == us_b_new

def test_project_detail_backlog_controller_move_user_story_up():
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

    project_detail_controller.handle(config.ProjectBacklogKeys.US_UP)
    assert project_view.backlog.notifier.info_msg.call_count == 1

    us_b_new = project_detail_controller.backlog.user_stories[0]
    us_a_new = project_detail_controller.backlog.user_stories[1]

    assert us_a_old == us_a_new
    assert us_b_old == us_b_new

def test_project_detail_backlog_controller_update_user_stories_order_with_errors():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.backlog.notifier = mock.Mock()
    executor = factories.patched_executor(update_user_stories_order_response=factories.future(None))
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)

    project_detail_controller.handle(config.ProjectBacklogKeys.UPDATE_USER_STORIES_ORDER)
    assert project_view.backlog.notifier.error_msg.call_count == 1

def test_project_detail_backlog_controller_update_user_stories_order_with_success():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.backlog.notifier = mock.Mock()
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_view.backlog.notifier.reset_mock()

    project_detail_controller.handle(config.ProjectBacklogKeys.UPDATE_USER_STORIES_ORDER)
    assert project_view.backlog.notifier.info_msg.call_count == 1

def test_project_detail_backlog_controller_delete_user_story_with_errors():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.backlog.notifier = mock.Mock()
    executor = factories.patched_executor(delete_user_story_response=factories.future(None))
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)

    project_detail_controller.handle(config.ProjectBacklogKeys.DELETE_USER_STORY)
    assert project_view.backlog.notifier.error_msg.call_count == 1
    assert (executor.delete_user_story.call_args.call_list()[0][0][0]["id"] ==
            project_detail_controller.backlog.user_stories[0]["id"])

def test_project_detail_backlog_controller_delete_user_story_order_with_success():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.backlog.notifier = mock.Mock()
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_view.backlog.notifier.reset_mock()

    project_detail_controller.handle(config.ProjectBacklogKeys.DELETE_USER_STORY)
    assert project_view.backlog.notifier.info_msg.call_count == 1
    assert (executor.delete_user_story.call_args.call_list()[0][0][0]["id"] ==
            project_detail_controller.backlog.user_stories[0]["id"])
