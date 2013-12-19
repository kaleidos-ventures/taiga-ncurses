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
    def milestone_stats(self, id, project):
        return self.pool.submit(self.client.get_milestone_stats, id=id, params={"project": project["id"]})

    # User Stories
    def create_user_story(self, data):
        return self.pool.submit(self.client.create_user_story, data_dict=data)

    def update_user_stories_order(self, user_stories, project):
        data = {
            "projectId": project["id"],
            "bulkStories": [[v["id"], i] for i, v in enumerate(user_stories)]
        }
        return self.pool.submit(self.client.update_user_stories_order, data_dict=data)

    def unassigned_user_stories(self, project):
        return self.pool.submit(self.client.get_user_stories, params={"project": project["id"],
                                                                      "milestone__isnull": True})

    def user_stories(self, id,  project):
        return self.pool.submit(self.client.get_user_stories, params={"project": project["id"],
                                                                      "milestone": id})

    # Task
    #TODO

    # Issues
    def issues(self, project, order_by=[]):
        params = {"project": project["id"]}

        if order_by:
            params["order_by"] = ", ".join(order_by)

        return self.pool.submit(self.client.get_issues, params=params)

    # Wiki
    def wiki_pages(self, project):
        return self.pool.submit(self.client.get_wiki_pages, params={"project": project["id"]})

