from unittest import mock
from concurrent.futures import Future
import json

from gmncurses.ui import views, signals
from gmncurses.executor import Executor

from . import fixtures

# Auth
def login_view(username, password):
    login_view = views.auth.LoginView("username", "password")
    login_view._username_editor.set_edit_text(username)
    login_view._password_editor.set_edit_text(password)
    return login_view

def successful_login_response(username):
    return {
        'auth_token': 'eyJ1c2VyX2lkIjoxfQ:1Vmjdp:ILIJVRazEdK_pObFedQc2aZNWd0',
        'color': '',
        'default_language': '',
        'default_timezone': '',
        'description': '',
        'email': 'niwi@niwi.be',
        'first_name': '',
        'full_name': 'admin',
        'id': 1,
        'is_active': True,
        'last_name': '',
        'notify_changes_by_me': False,
        'notify_level': 'all_owned_projects',
        'photo': '',
        'projects': [],
        'username': username,
    }

# Projects
def projects():
    return json.loads(fixtures.PROJECTS)

def project(**kwargs):
    defaults = json.loads(fixtures.PROJECT)
    defaults.update(kwargs)
    return defaults

def project_stats():
    return json.loads(fixtures.PROJECT_STATS)

def project_issues_stats():
    return json.loads(fixtures.PROJECT_ISSUES_STATS)

# Milestones
def milestone():
    return json.loads(fixtures.MILESTONE)

def milestone_stats():
    return json.loads(fixtures.MILESTONE_STATS)

# User Stories
def unassigned_user_stories():
    return json.loads(fixtures.UNASSIGNED_USER_STORIES)

def user_stories():
    return json.loads(fixtures.USER_STORIES)

# Tasks
def milestone_tasks():
    return json.loads(fixtures.MILESTONE_TASKS)

# Issues
def issues():
    return json.loads(fixtures.ISSUES)

# Wiki
def wiki_pages():
    return json.loads(fixtures.WIKI_PAGES)

def future(value):
    f = Future()
    f.set_result(value)
    return f

def patched_executor(login_response=future(successful_login_response("admin")),
                     projects=future(projects()),
                     project_detail=future(project()),
                     project_stats=future(project_stats()),
                     unassigned_user_stories=future(unassigned_user_stories()),
                     milestone=future(milestone_stats()),
                     milestone_stats=future(milestone_stats()),
                     user_stories=future(user_stories()),
                     milestone_tasks=future(milestone_tasks()),
                     project_issues_stats=future(project_issues_stats()),
                     issues=future(issues()),
                     wiki_pages=future(wiki_pages())):
    executor = Executor(mock.Mock())
    executor.login = mock.Mock(return_value=login_response)
    executor.projects = mock.Mock(return_value=projects)
    executor.project_detail = mock.Mock(return_value=project_detail)
    executor.project_stats = mock.Mock(return_value=project_stats)
    executor.unassigned_user_stories = mock.Mock(return_value=unassigned_user_stories)
    executor.milestone = mock.Mock(return_value=milestone)
    executor.milestone_stats = mock.Mock(return_value=milestone_stats)
    executor.user_stories = mock.Mock(return_value=user_stories)
    executor.milestone_tasks = mock.Mock(return_value=milestone_tasks)
    executor.project_issues_stats = mock.Mock(return_value=project_issues_stats)
    executor.issues = mock.Mock(return_value=issues)
    executor.wiki_pages = mock.Mock(return_value=wiki_pages)

    return executor
