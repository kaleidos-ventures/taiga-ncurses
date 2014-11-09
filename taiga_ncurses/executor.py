# -*- coding: utf-8 -*-

"""
taiga_ncurses.executor
~~~~~~~~~~~~~~~~~~~~~~
"""

from concurrent.futures import ThreadPoolExecutor


class Executor:
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
    def milestone(self, milestone, project):
        params = {"project": project["id"]}

        return self.pool.submit(self.client.get_milestone, id=milestone["id"], params=params)

    def milestone_stats(self, milestone, project):
        params = {"project": project["id"]}

        return self.pool.submit(self.client.get_milestone_stats, id=milestone["id"], params=params)

    # User Stories
    def create_user_story(self, data):
        return self.pool.submit(self.client.create_user_story, data_dict=data)

    def create_user_stories_in_bulk(self, data):
        return self.pool.submit(self.client.create_user_stories_in_bulk, data_dict=data)

    def update_user_story(self, user_story, data):
        return self.pool.submit(self.client.update_user_story, id=user_story["id"], data_dict=data)

    def delete_user_story(self, user_story):
        return self.pool.submit(self.client.delete_user_story, id=user_story["id"])

    def update_user_stories_order(self, user_stories, project):
        data = {
            "projectId": project["id"],
            "bulkStories": [[v["id"], i] for i, v in enumerate(user_stories)]
        }
        return self.pool.submit(self.client.update_user_stories_order, data_dict=data)

    def unassigned_user_stories(self, project):
        params = {
            "project": project["id"],
            "milestone": None
        }

        return self.pool.submit(self.client.get_user_stories, params=params)

    def user_stories(self, milestone,  project):
        params = {
            "project": project["id"],
            "milestone": milestone["id"]
        }

        return self.pool.submit(self.client.get_user_stories, params=params)

    # Task
    def tasks(self, milestone, project):
        params = {
            "project": project["id"],
            "milestone": milestone["id"]
        }

        return self.pool.submit(self.client.get_tasks, params=params)

    def create_task(self, data):
        return self.pool.submit(self.client.create_task, data_dict=data)

    def update_task(self, task, data):
        return self.pool.submit(self.client.update_task, id=task["id"], data_dict=data)

    def delete_task(self, task):
        return self.pool.submit(self.client.delete_task, id=task["id"])

    # Issues
    def issues(self, project, order_by=[], filters={}):
        params = {"project": project["id"]}

        if order_by:
            params["order_by"] = ", ".join(order_by)

        if filters:
            params.update(filters)

        return self.pool.submit(self.client.get_issues, params=params)

    def create_issue(self, data):
        return self.pool.submit(self.client.create_issue, data_dict=data)

    def update_issue(self, issue, data):
        return self.pool.submit(self.client.update_issue, id=issue["id"], data_dict=data)

    def delete_issue(self, issue):
        return self.pool.submit(self.client.delete_issue, id=issue["id"])

    # Wiki
    def wiki_pages(self, project):
        params={"project": project["id"]}

        return self.pool.submit(self.client.get_wiki_pages, params=params)
