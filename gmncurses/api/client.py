# -*- coding: utf-8 -*-

"""
gmncurses.api.client
~~~~~~~~~~~~~~~~~~~~
"""

from urllib.parse import urljoin
import json

import requests


class BaseClient(object):
    """ Tha base class for an API client. """

    BASE_HEADERS = {
        "content-type": "application/json; charset: utf8",
        "X-DISABLE-PAGINATION": "true",
    }

    def __init__(self, host):
        self._host = host
        self._headers = self.BASE_HEADERS
        self.last_error = {}

    def _get(self, url, params, **kwargs):
        response = requests.get(url, params=params, headers=self._headers)
        data = json.loads(response.content.decode())

        if response.status_code == 200:
            return data

        self.last_error = {
            "status_code": response.status_code,
            "detail": data.get("detail", "")
        }
        return None

    def _post(self, url, data_dict, params, **kwargs):
        rdata = json.dumps(data_dict)

        response = requests.post(url, data=rdata, params=params, headers=self._headers)
        data = json.loads(response.content.decode())

        if response.status_code == 200:
            return data

        self.last_error = {
            "status_code": response.status_code,
            "detail": data.get("detail", "")
        }
        return None

    def _patch(self, url, data_dict, params, **kwargs):
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


class GreenMineClient(BaseClient):
    """ A Greenmine Api Client.

    >>> from gmncurses.api.client import *
    >>> api = GreenMineClient("http://localhost:8000")
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
        "milestones": "/api/v1/milestones",
        "milestone":  "/api/v1/milestones/{}",
        "user_stories": "/api/v1/userstories",
        "user_story":  "/api/v1/userstories/{}",
        "tasks": "/api/v1/tasks",
        "task":  "/api/v1/tasks/{}",
        "issues": "/api/v1/issues",
        "issue":  "/api/v1/issues/{}",
        "wiki_pages": "/api/v1/wiki_pages",
        "wiki_page":  "/api/v1/wiki_pages/{}",
    }

    # AUTHENTICATIONS
    @property
    def is_authenticated(self):
        return "Authorization" in self._headers

    def set_auth_token(self, auth_token):
        self._headers["Authorization"] = "Bearer {}".format(auth_token)

    def login(self, username, password, params={}, **kwargs):
        url = urljoin(self._host, self.URLS.get("auth"))
        data_dict = {
            "username": username,
            "password": password,
        }
        data = self._post(url, data_dict, params, **kwargs)

        if data and "auth_token" in data:
            self.set_auth_token(data["auth_token"])
        return data

    def logout(self):
        self._headers = self.BASE_HEADERS
        return True

    # USER

    def get_users(self, params={}, **kwargs):
        url = urljoin(self._host, self.URLS.get("users"))
        return self._get(url, params, **kwargs)

    def update_user(self, id, data_dict={}, params={}, **kwargs):
        url = urljoin(self._host, self.URLS.get("user").format(id))
        return self._patch(url, data_dict, params, **kwargs)

    def get_user(self, id, params={}, **kwargs):
        url = urljoin(self._host, self.URLS.get("user").format(id))
        return self._get(url, params, **kwargs)

    # PROJECT

    def get_projects(self, params={}, **kwargs):
        url = urljoin(self._host, self.URLS.get("projects"))
        return self._get(url, params, **kwargs)

    def create_project(self, data_dict={}, params={}, **kwargs):
        url = urljoin(self._host, self.URLS.get("projects"))
        return self._post(url, data_dict, params, **kwargs)

    def update_project(self, id, data_dict={}, params={}, **kwargs):
        url = urljoin(self._host, self.URLS.get("project").format(id))
        return self._patch(url, data_dict, params, **kwargs)

    def get_project(self, id, params={}, **kwargs):
        url = urljoin(self._host, self.URLS.get("project").format(id))
        return self._get(url, params, **kwargs)

    def get_project_stats(self, id, params={}, **kwargs):
        url = urljoin(self._host, self.URLS.get("project-stats").format(id))
        return self._get(url, params, **kwargs)

    # MILESTONE

    def get_milestones(self, params={}, **kwargs):
        url = urljoin(self._host, self.URLS.get("milestones"))
        return self._get(url, params, **kwargs)

    def create_milestone(self, data_dict={}, params={}, **kwargs):
        url = urljoin(self._host, self.URLS.get("milestones"))
        return self._post(url, data_dict, params, **kwargs)

    def update_milestone(self, id, data_dict={}, params={}, **kwargs):
        url = urljoin(self._host, self.URLS.get("milestone").format(id))
        return self._patch(url, data_dict, params, **kwargs)

    def get_milestone(self, id, params={}, **kwargs):
        url = urljoin(self._host, self.URLS.get("milestone").format(id))
        return self._get(url, params, **kwargs)

    # USER STORY

    def get_user_stories(self, params={}, **kwargs):
        url = urljoin(self._host, self.URLS.get("user_stories"))
        return self._get(url, params, **kwargs)

    def create_user_story(self, data_dict={}, params={}, **kwargs):
        url = urljoin(self._host, self.URLS.get("user_stories"))
        return self._post(url, data_dict, params, **kwargs)

    def update_user_story(self, id, data_dict={}, params={}, **kwargs):
        url = urljoin(self._host, self.URLS.get("user_story").format(id))
        return self._patch(url, data_dict, params, **kwargs)

    def get_user_story(self, id, params={}, **kwargs):
        url = urljoin(self._host, self.URLS.get("user_story").format(id))
        return self._get(url, params, **kwargs)

    # TASK

    def get_tasks(self, params={}, **kwargs):
        url = urljoin(self._host, self.URLS.get("tasks"))
        return self._get(url, params, **kwargs)

    def create_task(self, data_dict={}, params={}, **kwargs):
        url = urljoin(self._host, self.URLS.get("tasks"))
        return self._post(url, data_dict, params, **kwargs)

    def update_task(self, id, data_dict={}, params={}, **kwargs):
        url = urljoin(self._host, self.URLS.get("task").format(id))
        return self._patch(url, data_dict, params, **kwargs)

    def get_task(self, id, params={}, **kwargs):
        url = urljoin(self._host, self.URLS.get("task").format(id))
        return self._get(url, params, **kwargs)

    # ISSUE

    def get_issues(self, params={}, **kwargs):
        url = urljoin(self._host, self.URLS.get("issues"))
        return self._get(url, params, **kwargs)

    def create_issue(self, data_dict={}, params={}, **kwargs):
        url = urljoin(self._host, self.URLS.get("issues"))
        return self._post(url, data_dict, params, **kwargs)

    def update_issue(self, id, data_dict={}, params={}, **kwargs):
        url = urljoin(self._host, self.URLS.get("issue").format(id))
        return self._patch(url, data_dict, params, **kwargs)

    def get_issue(self, id, params={}, **kwargs):
        url = urljoin(self._host, self.URLS.get("issue").format(id))
        return self._get(url, params, **kwargs)

    # WIKI PAGE

    def get_wiki_pages(self, params={}, **kwargs):
        url = urljoin(self._host, self.URLS.get("wiki_pages"))
        return self._get(url, params, **kwargs)

    def create_wiki_page(self, data_dict={}, params={}, **kwargs):
        url = urljoin(self._host, self.URLS.get("wiki_pages"))
        return self._post(url, data_dict, params, **kwargs)

    def update_wiki_page(self, id, data_dict={}, params={}, **kwargs):
        url = urljoin(self._host, self.URLS.get("wiki_page").format(id))
        return self._patch(url, data_dict, params, **kwargs)

    def get_wiki_page(self, id, params={}, **kwargs):
        url = urljoin(self._host, self.URLS.get("wiki_page").format(id))
        return self._get(url, params, **kwargs)
