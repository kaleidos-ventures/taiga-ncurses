# -*- coding: utf-8 -*-

import json
import requests


class GMApiClient(object):
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
    }

    def __init__(self, host):
        self._host = host
        self._headers = self.BASE_HEADERS
        self.user = None
        self.last_error = {}

    def login(self, username, password):
        url = self._host + self.URLS.get("auth")

        rdata = json.dumps({
            "username": username,
            "password": password,
        })

        response = requests.post(url, data=rdata, headers=self._headers)
        data = json.loads(response.content.decode())

        if response.status_code == 200:
            self.user = data
            self._headers["Authorization"] = "Bearer {}".format(self.user.get("auth_token", ""))
            return True

        self.last_error = {
            "status_code": response.status_code,
            "detail": data.get("detail", "")
        }
        return False

    def logout(self):
        self._headers = self.BASE_HEADERS
        self.user = None
        return True

    def get_projects(self):
        url = self._host + self.URLS.get("projects")

        response = requests.get(url, headers=self._headers)
        data = json.loads(response.content.decode())

        if response.status_code == 200:
            return data

        self.last_error = {
            "status_code": response.status_code,
            "detail": data.get("detail", "")
        }
        return False

    def get_project(self, id):
        url = self._host + self.URLS.get("project").format(id)

        response = requests.get(url, headers=self._headers)
        data = json.loads(response.content.decode())

        if response.status_code == 200:
            return data

        self.last_error = {
            "status_code": response.status_code,
            "detail": data.get("detail", "")
        }
        return False
