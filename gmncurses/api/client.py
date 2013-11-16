# -*- coding: utf-8 -*-

import json
import requests


class GreenMmine(object):
    """ A Greenmine Api Client.

    >>> from gmncurses.api.client import *
    >>> api = GreenMine("http://localhost:8000")
    >>> api.login("admin", "123123")
    {...}
    >>> api.get_projets()
    [...]
    >>> api.get_task(1)
    {...}
    >>> api.get_issue(1234)
    False
    >>> api.last_error
    {'detail': 'Not found', 'status_code': 404}

    """
    BASE_HEADERS = {
        "content-type": "application/json; charset: utf8",
        "X-DISABLE-PAGINATION": "true"
    }

    URLS = {
        "auth": "/api/v1/auth",
        "users": "/api/v1/users",
        "user":  "/api/v1/users/{}",
        "projects": "/api/v1/projects",
        "project":  "/api/v1/projects/{}",
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

    def __init__(self, host):
        self._host = host
        self._headers = self.BASE_HEADERS
        self.user = None
        self.last_error = {}

    def _get(self, url, on_success_callback=None, error_callback=None):
        response = requests.get(url, headers=self._headers)
        data = json.loads(response.content.decode())

        if response.status_code == 200:
            if on_success_callback:
                return on_success_callback(data)
            return data

        self.last_error = {
            "status_code": response.status_code,
            "detail": data.get("detail", "")
        }
        if error_callback:
            return error_callback(data)
        return False

    def _post(self, url, data_dict, on_success_callback=None, error_callback=None):
        rdata = json.dumps(data_dict)

        response = requests.post(url, data=rdata, headers=self._headers)
        data = json.loads(response.content.decode())

        if response.status_code == 200:
            if on_success_callback:
                return on_success_callback(data)
            return data

        self.last_error = {
            "status_code": response.status_code,
            "detail": data.get("detail", "")
        }
        if error_callback:
            return error_callback(data)
        return False

    def login(self, username, password):
        def auth_on_success(data):
            self.user = data
            self._headers["Authorization"] = "Bearer {}".format(self.user.get("auth_token", ""))
            return data

        url = self._host + self.URLS.get("auth")
        data_dict = {
            "username": username,
            "password": password,
        }
        return self._post(url, data_dict, on_success_callback=auth_on_success)

    def logout(self):
        self._headers = self.BASE_HEADERS
        self.user = None
        return True

    def get_users(self):
        url = self._host + self.URLS.get("users")
        return self._get(url)

    def get_user(self, id):
        url = self._host + self.URLS.get("user").format(id)
        return self._get(url)

    def get_projects(self):
        url = self._host + self.URLS.get("projects")
        return self._get(url)

    def get_project(self, id):
        url = self._host + self.URLS.get("project").format(id)
        return self._get(url)

    def get_milestones(self):
        url = self._host + self.URLS.get("milestones")
        return self._get(url)

    def get_milestone(self, id):
        url = self._host + self.URLS.get("milestone").format(id)
        return self._get(url)

    def get_user_stories(self):
        url = self._host + self.URLS.get("user_stories")
        return self._get(url)

    def get_user_story(self, id):
        url = self._host + self.URLS.get("user_story").format(id)
        return self._get(url)

    def get_tasks(self):
        url = self._host + self.URLS.get("tasks")
        return self._get(url)

    def get_task(self, id):
        url = self._host + self.URLS.get("task").format(id)
        return self._get(url)

    def get_issues(self):
        url = self._host + self.URLS.get("issues")
        return self._get(url)

    def get_issue(self, id):
        url = self._host + self.URLS.get("issue").format(id)
        return self._get(url)

    def get_wiki_pages(self):
        url = self._host + self.URLS.get("wiki_pages")
        return self._get(url)

    def get_wiki_page(self, id):
        url = self._host + self.URLS.get("wiki_page").format(id)
        return self._get(url)
