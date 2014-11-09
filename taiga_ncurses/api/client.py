# -*- coding: utf-8 -*-

"""
taiga_ncurses.api.client
~~~~~~~~~~~~~~~~~~~~~~~~
"""

from urllib.parse import urljoin
import json

import requests


class BaseClient:
    """ The base class for an API client. """

    BASE_HEADERS = {
        "content-type": "application/json; charset: utf8",
        "X-DISABLE-PAGINATION": "true",
    }

    def __init__(self, host):
        self._host = host
        self._headers = self.BASE_HEADERS
        self.last_error = {}

    def _get(self, url, params):
        response = requests.get(url, params=params, headers=self._headers)
        data = json.loads(response.content.decode())

        if response.status_code == 200:
            return data

        self.last_error = {
            "status_code": response.status_code,
            "detail": data.get("detail", "")
        }
        return None

    def _post(self, url, data_dict, params):
        rdata = json.dumps(data_dict)

        response = requests.post(url, data=rdata, params=params, headers=self._headers)

        if response.status_code in [200, 201]:
            data = json.loads(response.content.decode())
            return data
        elif response.status_code == 204: # No content
            return True
        else:
            data = json.loads(response.content.decode())

        self.last_error = {
            "status_code": response.status_code,
            "detail": data.get("detail", "")
        }
        return None

    def _patch(self, url, data_dict, params):
        rdata = json.dumps(data_dict)

        response = requests.patch(url, data=rdata, params=params, headers=self._headers)
        data = json.loads(response.content.decode())

        if response.status_code == 200:
            return data

        self.last_error = {
            "status_code": response.status_code,
            "detail": data.get("detail", "")
        }
        return None

    def _delete(self, url, params):
        response = requests.delete(url, params=params, headers=self._headers)

        if response.status_code == 204:
            return True

        data = json.loads(response.content.decode())

        self.last_error = {
            "status_code": response.status_code,
            "detail": data.get("detail", "")
        }
        return None


class TaigaClient(BaseClient):
    """ A Taiga Api Client.

    >>> from taiga_ncurses.api.client import *
    >>> api = TaigaClient("http://localhost:8000")
    >>> api.login("admin", "123123")
    {...}
    >>> api.get_projects()
    [...]
    >>> api.get_project(1)
    {...}
    >>> api.get_user_stories(params={'project': 1})
    [...]
    >>> api.get_issue(1234)
    None
    >>> api.last_error
    {'detail': 'Not found', 'status_code': 404}

    """

    URLS = {
        "auth": "/api/v1/auth",
        "users": "/api/v1/users",
        "user":  "/api/v1/users/{}",
        "projects": "/api/v1/projects",
        "project":  "/api/v1/projects/{}",
        "project-stats": "/api/v1/projects/{}/stats",
        "project-issues-stats": "/api/v1/projects/{}/issues_stats",
        "milestones": "/api/v1/milestones",
        "milestone":  "/api/v1/milestones/{}",
        "milestone-stats":  "/api/v1/milestones/{}/stats",
        "user_stories": "/api/v1/userstories",
        "user_stories_bulk_create": "/api/v1/userstories/bulk_create",
        "user_stories_bulk_update_order": "/api/v1/userstories/bulk_update_order",
        "user_story":  "/api/v1/userstories/{}",
        "tasks": "/api/v1/tasks",
        "task":  "/api/v1/tasks/{}",
        "issues": "/api/v1/issues",
        "issue":  "/api/v1/issues/{}",
        "wiki_pages": "/api/v1/wiki",
        "wiki_page":  "/api/v1/wiki/{}",
    }

    # AUTHENTICATIONS
    def __init__(self, host):
        super().__init__(host)

    @property
    def is_authenticated(self):
        return "Authorization" in self._headers

    def set_auth_token(self, auth_token):
        self._headers["Authorization"] = "Bearer {}".format(auth_token)

    def login(self, username, password, params={}):
        url = urljoin(self._host, self.URLS.get("auth"))
        data_dict = {
            "username": username,
            "password": password,
            "type": "normal"
        }
        data = self._post(url, data_dict, params)

        if data and "auth_token" in data:
            self.set_auth_token(data["auth_token"])
        return data

    def logout(self):
        self._headers = self.BASE_HEADERS
        return True

    # USER

    def get_users(self, params={}):
        url = urljoin(self._host, self.URLS.get("users"))
        return self._get(url, params)

    def update_user(self, id, data_dict={}, params={}):
        url = urljoin(self._host, self.URLS.get("user").format(id))
        return self._patch(url, data_dict, params)

    def get_user(self, id, params={}):
        url = urljoin(self._host, self.URLS.get("user").format(id))
        return self._get(url, params)

    # PROJECT

    def get_projects(self, params={}):
        url = urljoin(self._host, self.URLS.get("projects"))
        return self._get(url, params)

    def create_project(self, data_dict={}, params={}):
        url = urljoin(self._host, self.URLS.get("projects"))
        return self._post(url, data_dict, params)

    def update_project(self, id, data_dict={}, params={}):
        url = urljoin(self._host, self.URLS.get("project").format(id))
        return self._patch(url, data_dict, params)

    def get_project(self, id, params={}):
        url = urljoin(self._host, self.URLS.get("project").format(id))
        return self._get(url, params)

    def delete_project(self, id, params={}):
        url = urljoin(self._host, self.URLS.get("project").format(id))
        return self._delete(url, params)

    def get_project_stats(self, id, params={}):
        url = urljoin(self._host, self.URLS.get("project-stats").format(id))
        return self._get(url, params)

    def get_project_issues_stats(self, id, params={}):
        url = urljoin(self._host, self.URLS.get("project-issues-stats").format(id))
        return self._get(url, params)

    # MILESTONE

    def get_milestones(self, params={}):
        url = urljoin(self._host, self.URLS.get("milestones"))
        return self._get(url, params)

    def create_milestone(self, data_dict={}, params={}):
        url = urljoin(self._host, self.URLS.get("milestones"))
        return self._post(url, data_dict, params)

    def update_milestone(self, id, data_dict={}, params={}):
        url = urljoin(self._host, self.URLS.get("milestone").format(id))
        return self._patch(url, data_dict, params)

    def get_milestone(self, id, params={}):
        url = urljoin(self._host, self.URLS.get("milestone").format(id))
        return self._get(url, params)

    def delete_milestone(self, id, params={}):
        url = urljoin(self._host, self.URLS.get("milestone").format(id))
        return self._delete(url, params)

    def get_milestone_stats(self, id, params={}):
        url = urljoin(self._host, self.URLS.get("milestone-stats").format(id))
        return self._get(url, params)


    # USER STORY

    def get_user_stories(self, params={}):
        url = urljoin(self._host, self.URLS.get("user_stories"))
        return self._get(url, params)

    def update_user_stories_order(self, data_dict={}, params={}):
        url = urljoin(self._host, self.URLS.get("user_stories_bulk_update_order"))
        return self._post(url, data_dict, params)

    def create_user_stories_in_bulk(self, data_dict={}, params={}):
        url = urljoin(self._host, self.URLS.get("user_stories_bulk_create"))
        return self._post(url, data_dict, params)

    def create_user_story(self, data_dict={}, params={}):
        url = urljoin(self._host, self.URLS.get("user_stories"))
        return self._post(url, data_dict, params)

    def update_user_story(self, id, data_dict={}, params={}):
        url = urljoin(self._host, self.URLS.get("user_story").format(id))
        return self._patch(url, data_dict, params)

    def get_user_story(self, id, params={}):
        url = urljoin(self._host, self.URLS.get("user_story").format(id))
        return self._get(url, params)

    def delete_user_story(self, id, params={},):
        url = urljoin(self._host, self.URLS.get("user_story").format(id))
        return self._delete(url, params)

    # TASK

    def get_tasks(self, params={}):
        url = urljoin(self._host, self.URLS.get("tasks"))
        return self._get(url, params)

    def create_task(self, data_dict={}, params={}):
        url = urljoin(self._host, self.URLS.get("tasks"))
        return self._post(url, data_dict, params)

    def update_task(self, id, data_dict={}, params={}):
        url = urljoin(self._host, self.URLS.get("task").format(id))
        return self._patch(url, data_dict, params)

    def get_task(self, id, params={}):
        url = urljoin(self._host, self.URLS.get("task").format(id))
        return self._get(url, params)

    def delete_task(self, id, params={}):
        url = urljoin(self._host, self.URLS.get("task").format(id))
        return self._delete(url, params)

    # ISSUE

    def get_issues(self, params={}):
        url = urljoin(self._host, self.URLS.get("issues"))
        return self._get(url, params)

    def create_issue(self, data_dict={}, params={}):
        url = urljoin(self._host, self.URLS.get("issues"))
        return self._post(url, data_dict, params)

    def update_issue(self, id, data_dict={}, params={}):
        url = urljoin(self._host, self.URLS.get("issue").format(id))
        return self._patch(url, data_dict, params)

    def get_issue(self, id, params={}):
        url = urljoin(self._host, self.URLS.get("issue").format(id))
        return self._get(url, params)

    def delete_issue(self, id, params={}):
        url = urljoin(self._host, self.URLS.get("issue").format(id))
        return self._delete(url, params)

    # WIKI PAGE

    def get_wiki_pages(self, params={}):
        url = urljoin(self._host, self.URLS.get("wiki_pages"))
        return self._get(url, params)

    def create_wiki_page(self, data_dict={}, params={}):
        url = urljoin(self._host, self.URLS.get("wiki_pages"))
        return self._post(url, data_dict, params)

    def update_wiki_page(self, id, data_dict={}, params={}):
        url = urljoin(self._host, self.URLS.get("wiki_page").format(id))
        return self._patch(url, data_dict, params)

    def get_wiki_page(self, id, params={}):
        url = urljoin(self._host, self.URLS.get("wiki_page").format(id))
        return self._get(url, params)

    def delete_wiki_page(self, id, params={}):
        url = urljoin(self._host, self.URLS.get("wiki_page").format(id))
        return self._delete(url, params)
