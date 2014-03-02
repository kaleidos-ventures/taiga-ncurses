from unittest import mock
from concurrent.futures import Future
import json

from taiga_ncurses.ui import views, signals
from taiga_ncurses.executor import Executor

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

def successful_create_user_story_response(subject):
    return {
        "tags": [],
        "points": {"4": 1, "1": 1, "2": 1, "3": 1},
        "total_points": 0.0,
        "comment": "",
        "id": 114,
        "ref": 30,
        "milestone": None,
        "project": 1,
        "owner": 1,
        "status": 1,
        "is_closed": False,
        "order": 100,
        "created_date": "2013-12-31T16:56:38.115Z",
        "modified_date": "2013-12-31T16:56:38.115Z",
        "finish_date": None,
        "subject": subject,
        "description": "",
        "client_requirement": False,
        "team_requirement": False,
        "watchers": []
    }

def successful_update_user_story_response(subject):
    return {
        "tags": [],
        "points": {"4": 1, "1": 1, "2": 1, "3": 1},
        "total_points": 0.0,
        "comment": "",
        "id": 114,
        "ref": 30,
        "milestone": None,
        "project": 1,
        "owner": 1,
        "status": 1,
        "is_closed": False,
        "order": 100,
        "created_date": "2013-12-31T16:56:38.115Z",
        "modified_date": "2013-12-31T16:56:38.115Z",
        "finish_date": None,
        "subject": subject,
        "description": "",
        "client_requirement": False,
        "team_requirement": False,
        "watchers": []
    }

def successful_create_user_stories_in_bulk_response():
    return True

def successful_update_user_stories_order_response():
    return True

def successful_delete_user_story_response():
    return True

# Tasks
def tasks():
    return json.loads(fixtures.MILESTONE_TASKS)

def successful_create_task_response(subject, user_story):
    return {
        "tags": "",
        "comment": "",
        "id": 35,
        "user_story": user_story,
        "ref": 36,
        "owner": 3,
        "status": 1,
        "project": 1,
        "milestone": 4,
        "created_date": "2013-12-20T09:53:53.462Z",
        "modified_date": "2013-12-26T16:54:54.931Z",
        "finished_date": None,
        "subject": subject,
        "description": "Praesentium tempora molestias quis autem iste. Esse perspiciatis eos odio nemo, accusamus adipisci doloremque nesciunt temporibus consequatur dolore tempora dolorum, necessitatibus fugiat non veniam mollitia adipisci nesciunt quibusdam accusamus quidem quis consequuntur, error sunt fugit dolorem suscipit, rem numquam dicta nemo sapiente.",
        "assigned_to": 9,
        "is_iocaine": False,
        "watchers": []
    }

def successful_update_task_response(subject, user_story):
    return {
        "tags": "",
        "comment": "",
        "id": 35,
        "user_story": user_story,
        "ref": 36,
        "owner": 3,
        "status": 1,
        "project": 1,
        "milestone": 4,
        "created_date": "2013-12-20T09:53:53.462Z",
        "modified_date": "2013-12-26T16:54:54.931Z",
        "finished_date": None,
        "subject": subject,
        "description": "Praesentium tempora molestias quis autem iste. Esse perspiciatis eos odio nemo, accusamus adipisci doloremque nesciunt temporibus consequatur dolore tempora dolorum, necessitatibus fugiat non veniam mollitia adipisci nesciunt quibusdam accusamus quidem quis consequuntur, error sunt fugit dolorem suscipit, rem numquam dicta nemo sapiente.",
        "assigned_to": 9,
        "is_iocaine": False,
        "watchers": []
    }

def successful_delete_task_response():
    return True

# Issues
def issues():
    return json.loads(fixtures.ISSUES)

def successful_create_issue_response(subject):
    return {
        "tags": [
            "ratione",
            "omnis",
            "saepe",
            "tempora",
            "repellat"
        ],
        "comment": "",
        "is_closed": False,
        "id": 1,
        "ref": 2,
        "owner": 2,
        "status": 7,
        "severity": 5,
        "priority": 2,
        "type": 2,
        "milestone": None,
        "project": 1,
        "created_date": "2013-12-20T09:53:59.044Z",
        "modified_date": "2013-12-20T09:53:59.609Z",
        "finished_date": None,
        "subject": subject,
        "description": "Alias voluptatem nulla quo reiciendis dicta distinctio, quis vel facilis quae dolore rerum earum error nesciunt, ipsam itaque eius placeat doloribus voluptate sequi? Impedit iure adipisci et itaque debitis nihil vel ipsum esse ut perspiciatis. Facilis fuga exercitationem illo ipsam eveniet, tempora assumenda voluptate, tenetur saepe doloribus beatae neque quae quasi culpa reprehenderit et, totam temporibus deleniti consectetur rerum quis eaque commodi.",
        "assigned_to": 1,
        "watchers": []
    }

def successful_update_issue_response(subject):
    return {
        "tags": [
            "ratione",
            "omnis",
            "saepe",
            "tempora",
            "repellat"
        ],
        "comment": "",
        "is_closed": False,
        "id": 1,
        "ref": 2,
        "owner": 2,
        "status": 7,
        "severity": 5,
        "priority": 2,
        "type": 2,
        "milestone": None,
        "project": 1,
        "created_date": "2013-12-20T09:53:59.044Z",
        "modified_date": "2013-12-20T09:53:59.609Z",
        "finished_date": None,
        "subject": subject,
        "description": "Alias voluptatem nulla quo reiciendis dicta distinctio, quis vel facilis quae dolore rerum earum error nesciunt, ipsam itaque eius placeat doloribus voluptate sequi? Impedit iure adipisci et itaque debitis nihil vel ipsum esse ut perspiciatis. Facilis fuga exercitationem illo ipsam eveniet, tempora assumenda voluptate, tenetur saepe doloribus beatae neque quae quasi culpa reprehenderit et, totam temporibus deleniti consectetur rerum quis eaque commodi.",
        "assigned_to": 1,
        "watchers": []
    }

def successful_delete_issue_response():
    return True

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
                     milestone=future(milestone()),
                     milestone_stats=future(milestone_stats()),
                     user_stories=future(user_stories()),
                     create_user_story_response=future(successful_create_user_story_response("Create us")),
                     update_user_story_response=future(successful_update_user_story_response("Update us")),
                     create_user_stories_in_bulk_response=future(
                            successful_create_user_stories_in_bulk_response()),
                     update_user_stories_order_response=future(successful_update_user_stories_order_response()),
                     delete_user_story_response=future(successful_delete_user_story_response()),
                     tasks=future(tasks()),
                     create_task_response=future(successful_create_task_response("Create task", 1)),
                     update_task_response=future(successful_update_task_response("Update task", 1)),
                     delete_task_response=future(successful_delete_task_response()),
                     project_issues_stats=future(project_issues_stats()),
                     issues=future(issues()),
                     create_issue_response=future(successful_create_issue_response("Create issue")),
                     update_issue_response=future(successful_update_issue_response("Update issue")),
                     delete_issue_response=future(successful_delete_issue_response()),
                     wiki_pages=future(wiki_pages())):
    executor = Executor(mock.Mock())

    executor.login = mock.Mock(return_value=login_response)

    executor.projects = mock.Mock(return_value=projects)
    executor.project_detail = mock.Mock(return_value=project_detail)
    executor.project_stats = mock.Mock(return_value=project_stats)
    executor.project_issues_stats = mock.Mock(return_value=project_issues_stats)

    executor.user_stories = mock.Mock(return_value=user_stories)
    executor.unassigned_user_stories = mock.Mock(return_value=unassigned_user_stories)
    executor.create_user_story = mock.Mock(return_value=create_user_story_response)
    executor.update_user_story = mock.Mock(return_value=update_user_story_response)
    executor.create_user_stories_in_bulk = mock.Mock(return_value=create_user_stories_in_bulk_response)
    executor.update_user_stories_order = mock.Mock(return_value=update_user_stories_order_response)
    executor.delete_user_story = mock.Mock(return_value=delete_user_story_response)

    executor.milestone = mock.Mock(return_value=milestone)
    executor.milestone_stats = mock.Mock(return_value=milestone_stats)

    executor.tasks = mock.Mock(return_value=tasks)
    executor.create_task = mock.Mock(return_value=create_task_response)
    executor.update_task = mock.Mock(return_value=update_task_response)
    executor.delete_task = mock.Mock(return_value=delete_task_response)

    executor.issues = mock.Mock(return_value=issues)
    executor.create_issue = mock.Mock(return_value=create_issue_response)
    executor.update_issue = mock.Mock(return_value=update_issue_response)
    executor.delete_issue = mock.Mock(return_value=delete_issue_response)

    executor.wiki_pages = mock.Mock(return_value=wiki_pages)

    return executor
