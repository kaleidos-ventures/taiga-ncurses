from concurrent.futures import Future
from unittest import mock

from taiga_ncurses.ui import signals, views
from taiga_ncurses import controllers
from taiga_ncurses.config import settings
from taiga_ncurses.executor import Executor
from taiga_ncurses.core import StateMachine

from tests import factories


def test_issues_controller_show_the_filters_popup():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.issues)

    assert not hasattr(project_detail_controller.view.issues, "filters_popup")
    project_detail_controller.handle(settings.data.issues.keys.filters)
    assert hasattr(project_detail_controller.view.issues, "filters_popup")

def test_issues_controller_submit_the_filters_popup():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.issues.notifier = mock.Mock()
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.issues)
    project_detail_controller.handle(settings.data.issues.keys.filters)
    filters_popup = project_detail_controller.view.issues.filters_popup
    project_view.issues.notifier.reset_mock()
    executor.issues.reset_mock()

    assert project_view.issues.notifier.info_msg.call_count == 0
    assert executor.issues.call_count == 0
    filters_popup._issue_types_group[0].set_state(True)
    filters_popup._issue_statuses_group[0].set_state(True)
    filters_popup._priorities_group[0].set_state(True)
    filters_popup._severities_group[0].set_state(True)
    filters_popup._assigned_to_group[0].set_state(True)
    filters_popup._created_by_group[0].set_state(True)
    #filters_popup._tags_group[0].set_state(True)
    signals.emit(filters_popup.filter_button, "click")
    assert project_view.issues.notifier.info_msg.call_count == 1
    assert executor.issues.call_count == 1
    assert len(filters_popup._filters) == 7
    assert len(executor.issues.call_args.call_list()[0][1]["filters"]["type"]) == 1
    assert len(executor.issues.call_args.call_list()[0][1]["filters"]["status"]) == 1
    assert len(executor.issues.call_args.call_list()[0][1]["filters"]["severity"]) == 1
    assert len(executor.issues.call_args.call_list()[0][1]["filters"]["priority"]) == 1
    assert len(executor.issues.call_args.call_list()[0][1]["filters"]["assigned_to"]) == 1
    assert len(executor.issues.call_args.call_list()[0][1]["filters"]["owner"]) == 1
    #assert len(executor.issues.call_args.call_list()[0][1]["filters"]["tags"]) == 1

def test_issues_controller_cancel_the_filters_popup():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.issues)
    project_detail_controller.handle(settings.data.issues.keys.filters)

    assert hasattr(project_detail_controller.view.issues, "filters_popup")
    filters_popup = project_detail_controller.view.issues.filters_popup
    signals.emit(filters_popup.cancel_button, "click")
    assert not hasattr(project_detail_controller.view.issues, "filters_popup")

def test_issues_controller_show_the_help_popup():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.issues)

    assert not hasattr(project_detail_controller.view.issues, "help_popup")
    project_detail_controller.handle(settings.data.issues.keys.help)
    assert hasattr(project_detail_controller.view.issues, "help_popup")

def test_issues_controller_close_the_help_popup():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.issues)
    project_detail_controller.handle(settings.data.issues.keys.help)

    assert hasattr(project_detail_controller.view.issues, "help_popup")
    help_popup = project_detail_controller.view.issues.help_popup
    signals.emit(help_popup.close_button, "click")
    assert not hasattr(project_detail_controller.view.issues, "help_popup")

def test_issues_controller_reload():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.issues)
    executor.project_issues_stats.reset_mock()
    executor.issues.reset_mock()

    assert executor.project_issues_stats.call_count == 0
    assert executor.issues.call_count == 0
    project_detail_controller.handle(settings.data.issues.keys.reload)
    assert executor.project_issues_stats.call_count == 1
    assert executor.issues.call_count == 1

def test_issues_controller_show_the_new_issue_form():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.issues)

    assert not hasattr(project_detail_controller.view.issues, "issue_form")
    project_detail_controller.handle(settings.data.issues.keys.create)
    assert hasattr(project_detail_controller.view.issues, "issue_form")

def test_issues_controller_cancel_the_new_issue_form():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.issues)
    project_detail_controller.handle(settings.data.issues.keys.create)

    assert hasattr(project_detail_controller.view.issues, "issue_form")
    form = project_detail_controller.view.issues.issue_form
    signals.emit(form.cancel_button, "click")
    assert not hasattr(project_detail_controller.view.issues, "issue_form")

def test_issues_controller_submit_new_issue_form_with_errors():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.issues.notifier = mock.Mock()
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.issues)
    project_detail_controller.handle(settings.data.issues.keys.create)
    form = project_detail_controller.view.issues.issue_form

    signals.emit(form.save_button, "click")
    assert project_view.issues.notifier.error_msg.call_count == 1

def test_issues_controller_submit_new_issue_form_successfully():
    issue_subject = "Create a new issue"
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.issues.notifier = mock.Mock()
    executor = factories.patched_executor(create_issue_response=factories.future(
                           factories.successful_create_issue_response(issue_subject)))
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.issues)
    project_detail_controller.handle(settings.data.issues.keys.create)
    form = project_detail_controller.view.issues.issue_form
    project_view.issues.notifier.reset_mock()

    form._subject_edit.set_edit_text(issue_subject)
    signals.emit(form.save_button, "click")
    assert project_view.issues.notifier.info_msg.call_count == 1
    assert executor.create_issue.call_args.call_list()[0][0][0]["subject"] == issue_subject
    assert executor.create_issue.call_count == 1
    assert executor.create_issue.return_value.result()["subject"] == issue_subject

def test_issues_controller_show_the_edit_issue_form():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.issues)

    assert not hasattr(project_detail_controller.view.issues, "issue_form")
    project_detail_controller.handle(settings.data.issues.keys.edit)
    assert hasattr(project_detail_controller.view.issues, "issue_form")
    assert (project_detail_controller.view.issues.issue_form.issue ==
            project_detail_controller.view.issues.issues.list_walker.get_focus()[0].issue)

def test_issues_controller_cancel_the_edit_issue_form():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.issues)
    project_detail_controller.handle(settings.data.issues.keys.edit)

    assert hasattr(project_detail_controller.view.issues, "issue_form")
    form = project_detail_controller.view.issues.issue_form
    signals.emit(form.cancel_button, "click")
    assert not hasattr(project_detail_controller.view.issues, "issue_form")

def test_issues_controller_submit_the_edit_issue_form_with_errors():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.issues.notifier = mock.Mock()
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.issues)
    project_detail_controller.handle(settings.data.issues.keys.edit)
    form = project_detail_controller.view.issues.issue_form

    form._subject_edit.set_edit_text("")
    signals.emit(form.save_button, "click")
    assert project_view.issues.notifier.error_msg.call_count == 1

def test_issues_controller_submit_edit_issue_form_successfully():
    issue_subject = "Update a issue"
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.issues.notifier = mock.Mock()
    executor = factories.patched_executor(update_issue_response=factories.future(
                           factories.successful_update_issue_response(issue_subject)))
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.issues)
    project_detail_controller.handle(settings.data.issues.keys.edit)
    form = project_detail_controller.view.issues.issue_form
    project_view.issues.notifier.reset_mock()

    form._subject_edit.set_edit_text(issue_subject)

    signals.emit(form.save_button, "click")
    assert project_view.issues.notifier.info_msg.call_count == 1
    assert (executor.update_issue.call_args.call_list()[0][0][0]["id"] == form.issue["id"])
    assert executor.update_issue.call_args.call_list()[0][0][1]["subject"] == issue_subject
    assert executor.update_issue.call_count == 1
    assert executor.update_issue.return_value.result()["subject"] == issue_subject

def test_issues_controller_delete_issue_with_errors():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.issues.notifier = mock.Mock()
    executor = factories.patched_executor(delete_issue_response=factories.future(None))
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.issues)

    project_detail_controller.handle(settings.data.issues.keys.delete)
    assert project_view.issues.notifier.error_msg.call_count == 1
    assert (executor.delete_issue.call_args.call_list()[0][0][0]["id"] ==
            project_detail_controller.issues.issues[0]["id"])

def test_issues_controller_delete_issue_with_success():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.issues.notifier = mock.Mock()
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.issues)
    project_view.issues.notifier.reset_mock()

    project_detail_controller.handle(settings.data.issues.keys.delete)
    assert project_view.issues.notifier.info_msg.call_count == 1
    assert (executor.delete_issue.call_args.call_list()[0][0][0]["id"] ==
            project_detail_controller.issues.issues[0]["id"])

def test_issues_controller_change_issue_status():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.issues.notifier = mock.Mock()
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.issues)
    project_view.issues.notifier.reset_mock()

    issue = project_view.issues.issues.widget.contents()[0][0]
    combo = issue.base_widget.widget.contents[1][0]     # 1 => status
    item = combo.menu.get_item(0)                       # 0 => New
    combo.item_changed(item, True)

    assert project_view.issues.notifier.info_msg.call_count == 1
    assert executor.update_issue.call_args.call_list()[0][0][1]["status"] == item.value
    assert executor.update_issue.call_count == 1

def test_issues_controller_change_issue_priority():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.issues.notifier = mock.Mock()
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.issues)
    project_view.issues.notifier.reset_mock()

    issue = project_view.issues.issues.widget.contents()[0][0]
    combo = issue.base_widget.widget.contents[2][0]     # 2 => priority
    item = combo.menu.get_item(0)                       # 0 => Low
    combo.item_changed(item, True)

    assert project_view.issues.notifier.info_msg.call_count == 1
    assert executor.update_issue.call_args.call_list()[0][0][1]["priority"] == item.value
    assert executor.update_issue.call_count == 1

def test_issues_controller_change_issue_severity():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.issues.notifier = mock.Mock()
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.issues)
    project_view.issues.notifier.reset_mock()

    issue = project_view.issues.issues.widget.contents()[0][0]
    combo = issue.base_widget.widget.contents[3][0]     # 3 => severity
    item = combo.menu.get_item(0)                       # 0 => wishlist
    combo.item_changed(item, True)

    assert project_view.issues.notifier.info_msg.call_count == 1
    assert executor.update_issue.call_args.call_list()[0][0][1]["severity"] == item.value
    assert executor.update_issue.call_count == 1

def test_issues_controller_change_issue_assigned_to():
    project = factories.project()
    project_view = views.projects.ProjectDetailView(project)
    project_view.issues.notifier = mock.Mock()
    executor = factories.patched_executor()
    _ = mock.Mock()
    project_detail_controller = controllers.projects.ProjectDetailController(project_view, executor, _)
    project_detail_controller.handle(settings.data.main.keys.issues)
    project_view.issues.notifier.reset_mock()

    issue = project_view.issues.issues.widget.contents()[0][0]
    combo = issue.base_widget.widget.contents[4][0]     # 4 => assigned_to
    item = combo.menu.get_item(0)                       # 0
    combo.item_changed(item, True)

    assert project_view.issues.notifier.info_msg.call_count == 1
    assert executor.update_issue.call_args.call_list()[0][0][1]["assigned_to"] == item.value
    assert executor.update_issue.call_count == 1
