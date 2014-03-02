from unittest import mock
from concurrent.futures import Future

from taiga_ncurses import executor


# Auth
def test_login_method_returns_a_future():
    client = mock.Mock()
    e = executor.Executor(client)
    f = e.login("admin", "123123")
    assert isinstance(f, Future)

# Project
def test_projects_method_returns_a_future():
    client = mock.Mock()
    e = executor.Executor(client)
    f = e.projects()
    assert isinstance(f, Future)

def test_project_detail_method_returns_a_future():
    client = mock.Mock()
    e = executor.Executor(client)
    f = e.project_detail({"id": 123123})
    assert isinstance(f, Future)

def test_project_stats_method_returns_a_future():
    client = mock.Mock()
    e = executor.Executor(client)
    f = e.project_stats({"id": 123123})
    assert isinstance(f, Future)

def test_project_issues_stats_method_returns_a_future():
    client = mock.Mock()
    e = executor.Executor(client)
    f = e.project_issues_stats({"id": 123123})
    assert isinstance(f, Future)

# Milestones
def test_milestone_method_returns_a_future():
    client = mock.Mock()
    e = executor.Executor(client)
    f = e.milestone({"id": 123123}, {"id": 123123})
    assert isinstance(f, Future)

def test_milestone_stats_method_returns_a_future():
    client = mock.Mock()
    e = executor.Executor(client)
    f = e.milestone_stats({"id": 123123}, {"id": 123123})
    assert isinstance(f, Future)

# User Stories
def test_create_user_story_method_returns_a_future():
    client = mock.Mock()
    e = executor.Executor(client)
    f = e.create_user_story({"subject": "Foo Bar"})
    assert isinstance(f, Future)

def test_update_user_story_method_returns_a_future():
    client = mock.Mock()
    e = executor.Executor(client)
    f = e.update_user_story({"id": 123123}, {"subject": "Bar Foo"})
    assert isinstance(f, Future)

def test_delete_user_story_method_returns_a_future():
    client = mock.Mock()
    e = executor.Executor(client)
    f = e.delete_user_story({"id": 123123})
    assert isinstance(f, Future)

def test_create_user_stories_in_bulk_method_returns_a_future():
    client = mock.Mock()
    e = executor.Executor(client)
    f = e.create_user_stories_in_bulk({"ulkStories": "A\nB\nC", "projectId": 1})
    assert isinstance(f, Future)

def test_update_user_stories_order_method_returns_a_future():
    client = mock.Mock()
    e = executor.Executor(client)
    f = e.update_user_stories_order([{"id": 123123}, {"id": 456456}], {"id": 123123})
    assert isinstance(f, Future)

def test_unassigned_user_stories_method_returns_a_future():
    client = mock.Mock()
    e = executor.Executor(client)
    f = e.unassigned_user_stories({"id": 123123})
    assert isinstance(f, Future)

def test_user_stories_method_returns_a_future():
    client = mock.Mock()
    e = executor.Executor(client)
    f = e.user_stories({"id": 123123}, {"id": 123123})

# Task
def test_tasks_method_returns_a_future():
    client = mock.Mock()
    e = executor.Executor(client)
    f = e.tasks({"id": 123123}, {"id": 123123})
    assert isinstance(f, Future)

def test_create_task_method_returns_a_future():
    client = mock.Mock()
    e = executor.Executor(client)
    f = e.create_task({"subject": "Foo Bar"})
    assert isinstance(f, Future)

def test_update_task_method_returns_a_future():
    client = mock.Mock()
    e = executor.Executor(client)
    f = e.update_task({"id": 123123}, {"subject": "Bar Foo"})
    assert isinstance(f, Future)

def test_delete_task_method_returns_a_future():
    client = mock.Mock()
    e = executor.Executor(client)
    f = e.delete_task({"id": 123123})
    assert isinstance(f, Future)

# Issues
def test_issues_method_returns_a_future():
    client = mock.Mock()
    e = executor.Executor(client)
    f = e.issues({"id": 123123}, ["status"], {"status": 1})
    assert isinstance(f, Future)

def test_create_issue_method_returns_a_future():
    client = mock.Mock()
    e = executor.Executor(client)
    f = e.create_issue({"subject": "Foo Bar"})
    assert isinstance(f, Future)

def test_update_issue_method_returns_a_future():
    client = mock.Mock()
    e = executor.Executor(client)
    f = e.update_issue({"id": 123123}, {"subject": "Bar Foo"})
    assert isinstance(f, Future)

def test_delete_issue_method_returns_a_future():
    client = mock.Mock()
    e = executor.Executor(client)
    f = e.delete_issue({"id": 123123})
    assert isinstance(f, Future)

# Wiki
def test_wiki_pages_method_returns_a_future():
    client = mock.Mock()
    e = executor.Executor(client)
    f = e.wiki_pages({"id": 123123})
    assert isinstance(f, Future)

