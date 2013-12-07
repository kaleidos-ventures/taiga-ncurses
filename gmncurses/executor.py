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

    # Auth
    def login(self, username, password):
        return self.pool.submit(self.client.login, username, password)

    # Project
    def projects(self):
        return self.pool.submit(self.client.get_projects)

    def project_detail(self, project):
        return self.pool.submit(self.client.get_project, id=project["id"])

    def project_stats(self, project):
        return self.pool.submit(self.client.get_project_stats, id=project["id"])

    def project_issues_stats(self, project):
        return self.pool.submit(self.client.get_project_issues_stats, id=project["id"])

    # Milestones
    #TODO

    # User Stories
    def unassigned_user_stories(self, project):
        return self.pool.submit(self.client.get_user_stories, params={"project": project["id"],
                                                                      "milestone__isnull": True})

    # Task
    #TODO

    # Issues
    def issues(self, project):
        return self.pool.submit(self.client.get_issues, params={"project": project["id"]})

    # Wiki
    #TODO
