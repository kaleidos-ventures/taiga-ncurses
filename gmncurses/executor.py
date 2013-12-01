# -*- coding: utf-8 -*-

"""
gmncurses.executor
~~~~~~~~~~~~~~~~~~
"""

from concurrent.futures import ThreadPoolExecutor


class Executor(object):
    def __init__(self, client):
        self.client = client
        self.pool = ThreadPoolExecutor(2)

    def login(self, username, password):
        return self.pool.submit(self.client.login, username, password)

    def project_detail(self, project):
        return self.pool.submit(self.client.get_project, id=project["id"])
