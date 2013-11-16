# -*- coding: utf-8 -*-

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

    def _get(self, url, params, on_success_callback, error_callback, **kwargs):
        response = requests.get(url, params=params, headers=self._headers)
        data = json.loads(response.content.decode())

        if response.status_code == 200:
            if on_success_callback and hasattr(on_success_callback, "__call__"):
                return on_success_callback(data, **kwargs)
            return data

        self.last_error = {
            "status_code": response.status_code,
            "detail": data.get("detail", "")
        }
        if error_callback and hasattr(error_callback, "__call__"):
            return error_callback(data, **kwargs)
        return False

    def _post(self, url, data_dict, params, on_success_callback, error_callback, **kwargs):
        rdata = json.dumps(data_dict)

        response = requests.post(url, data=rdata, params=params, headers=self._headers)
        data = json.loads(response.content.decode())

        if response.status_code == 200:
            if on_success_callback and hasattr(on_success_callback, "__call__"):
                return on_success_callback(data, **kwargs)
            return data

        self.last_error = {
            "status_code": response.status_code,
            "detail": data.get("detail", "")
        }
        if error_callback and hasattr(error_callback, "__call__"):
            return error_callback(data, **kwargs)
        return False


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
    False
    >>> api.last_error
    {'detail': 'Not found', 'status_code': 404}

    """

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

    def login(self, username, password, params={}, on_success_callback=None,
              error_callback=None, **kwargs):
        url = urljoin(self._host, self.URLS.get("auth"))
        data_dict = {
            "username": username,
            "password": password,
        }
        data = self._post(url, data_dict, params, on_success_callback,
                          error_callback, **kwargs)

        if data:
            self._headers["Authorization"] = "Bearer {}".format(data.get("auth_token",""))
        return data

    def logout(self, params={}, data_dicti={}, on_success_callback=None,
               error_callback=None, **kwargs):
        self._headers = self.BASE_HEADERS
        return True

    def get_projects(self, params={}, data_dicti={}, on_success_callback=None,
                 error_callback=None, **kwargs):
        url = urljoin(self._host, self.URLS.get("projects"))
        return self._get(url, params, on_success_callback, error_callback, **kwargs)

    def get_project(self, id, params={}, data_dicti={}, on_success_callback=None,
                 error_callback=None, **kwargs):
        url = urljoin(self._host, self.URLS.get("project").format(id))
        return self._get(url, params, on_success_callback, error_callback, **kwargs)

    def get_users(self, params={}, data_dicti={}, on_success_callback=None,
                 error_callback=None, **kwargs):
        url = urljoin(self._host, self.URLS.get("users"))
        return self._get(url, params, on_success_callback, error_callback, **kwargs)

    def get_user(self, id, params={}, data_dicti={}, on_success_callback=None,
                 error_callback=None, **kwargs):
        url = urljoin(self._host, self.URLS.get("user").format(id))
        return self._get(url, params, on_success_callback, error_callback, **kwargs)

    def get_users(self, params={}, data_dicti={}, on_success_callback=None,
                  error_callback=None, **kwargs):
        url = urljoin(self._host, self.URLS.get("users"))
        return self._get(url, params, on_success_callback, error_callback, **kwargs)

    def get_user(self, id, params={}, data_dicti={}, on_success_callback=None,
                 error_callback=None, **kwargs):
        url = urljoin(self._host, self.URLS.get("user").format(id))
        return self._get(url, params, on_success_callback, error_callback, **kwargs)

    def get_milestones(self, params={}, data_dicti={}, on_success_callback=None,
                       error_callback=None, **kwargs):
        url = urljoin(self._host, self.URLS.get("milestones"))
        return self._get(url, params, on_success_callback, error_callback, **kwargs)

    def get_milestone(self, id, params={}, data_dicti={}, on_success_callback=None,
                      error_callback=None, **kwargs):
        url = urljoin(self._host, self.URLS.get("milestone").format(id))
        return self._get(url, params, on_success_callback, error_callback, **kwargs)

    def get_user_stories(self, params={}, data_dicti={}, on_success_callback=None,
                         error_callback=None, **kwargs):
        url = urljoin(self._host, self.URLS.get("user_stories"))
        return self._get(url, params, on_success_callback, error_callback, **kwargs)

    def get_user_story(self, id, params={}, data_dicti={}, on_success_callback=None,
                       error_callback=None, **kwargs):
        url = urljoin(self._host, self.URLS.get("user_story").format(id))
        return self._get(url, params, on_success_callback, error_callback, **kwargs)

    def get_tasks(self, params={}, data_dicti={}, on_success_callback=None,
                  error_callback=None, **kwargs):
        url = urljoin(self._host, self.URLS.get("tasks"))
        return self._get(url, params, on_success_callback, error_callback, **kwargs)

    def get_task(self, id, params={}, data_dicti={}, on_success_callback=None,
                 error_callback=None, **kwargs):
        url = urljoin(self._host, self.URLS.get("task").format(id))
        return self._get(url, params, on_success_callback, error_callback, **kwargs)

    def get_issues(self, params={}, data_dicti={}, on_success_callback=None,
                   error_callback=None, **kwargs):
        url = urljoin(self._host, self.URLS.get("issues"))
        return self._get(url, params, on_success_callback, error_callback, **kwargs)

    def get_issue(self, id, params={}, data_dicti={}, on_success_callback=None,
                  error_callback=None, **kwargs):
        url = urljoin(self._host, self.URLS.get("issue").format(id))
        return self._get(url, params, on_success_callback, error_callback, **kwargs)

    def get_wiki_pages(self, params={}, data_dicti={}, on_success_callback=None,
                       error_callback=None, **kwargs):
        url = urljoin(self._host, self.URLS.get("wiki_pages"))
        return self._get(url, params, on_success_callback, error_callback, **kwargs)

    def get_wiki_page(self, id, params={}, data_dicti={}, on_success_callback=None,
                      error_callback=None, **kwargs):
        url = urljoin(self._host, self.URLS.get("wiki_page").format(id))
        return self._get(url, params, on_success_callback, error_callback, **kwargs)
