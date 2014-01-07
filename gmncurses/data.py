# -*- coding: utf-8 -*-

"""
gmncurses.data
~~~~~~~~~~~~~~
"""

from datetime import datetime
from collections import OrderedDict
from operator import itemgetter

# Project

def total_points(project_stats):
    return project_stats.get("total_points", 0)

def assigned_points(project_stats):
    return project_stats.get("assigned_points", 0)

def defined_points(project_stats):
    return project_stats.get("defined_points", 0)

def defined_points_percentage(project_stats):
    try:
        return defined_points(project_stats) * 100 / total_points(project_stats)
    except ZeroDivisionError:
        return 0

def closed_points(project_stats):
    return  project_stats.get("closed_points", 0)

def doomline_limit_points(project_stats):
    return total_points(project_stats) - assigned_points(project_stats)

def points(project):
    dc = {str(p["id"]): p for p in project.get("points", [])}
    return OrderedDict(sorted(dc.items(), key=lambda t: t[1]["order"] ))

def total_sprints(project_stats):
    return project_stats.get("total_milestones", 0)

def completed_sprints(project):
    milestones = project.get("list_of_milestones", [])
    now = datetime.now()
    return [m for m in milestones if date(m["finish_date"]) < now]

def current_sprint(project):
    milestones = project.get("list_of_milestones", [])
    if milestones:
        return len(milestones)
    return "--"

def current_sprint_name(project):
    milestones = project.get("list_of_milestones", [])
    if milestones:
        return milestones[-1].get("name", "unknown")
    return "-----"

def current_sprint_id(project):
    milestones = project.get("list_of_milestones", [])
    if milestones:
        return milestones[-1].get("id", None)
    return "-----"

def computable_roles(project):
    dc = {str(r["id"]): r for r in project.get("roles", []) if r["computable"]} if "roles" in project else {}
    return OrderedDict(sorted(dc.items(), key=lambda t: t[1]["order"] ))

def list_of_milestones(project, reverse=True):
    return sorted(project.get("list_of_milestones", []), key=lambda m: m["finish_date"], reverse=reverse)

def milestones_are_equals(milestone1, milestone2):
    return milestone1.get("id", milestone1) == milestone2.get("id", milestone2)

def memberships(project):
    dc = {str(r["user"]): r for r in project.get("memberships", [])} if "memberships" in project else {}
    return OrderedDict(sorted(dc.items(), key=lambda t: t[1]["full_name"] ))


# User Stories

def us_ref(us):
    return us.get("ref", "--")

def us_subject(us):
    return us.get("subject", "------")

def us_total_points(us):
    return us.get("total_points", "--")

def us_statuses(project):
    dc = {str(p["id"]): p for p in project.get("us_statuses", [])}
    return OrderedDict(sorted(dc.items(), key=lambda t: t[1]["order"] ))

def us_status_with_color(us, project, default_color="#ffffff"):
    # FIXME: Improvement, get priorities from a project constant
    # TODO: Check that the color is in hex format
    us_status_id = us.get("status", None)
    if us_status_id:
        us_statuses = {str(p["id"]): p for p in project["us_statuses"]}
        try:
            return (us_statuses[str(us_status_id)]["color"] or default_color,
                    us_statuses[str(us_status_id)]["name"])
        except KeyError:
            pass
    return (default_color, "---")


def us_points_by_role(us, project, roles):
    # FIXME: Improvement, get project_points from a project constant
    # FIXME: Improvement, get rolesofrom a project constant
    us_points = us.get("points", [])
    project_points = {str(p["id"]): p for p in project["points"]}
    default_point = project["default_points"]

    points = []
    for role in roles:
        try:
            points.append(project_points[str(us_points[str(role["id"])])]["name"])
        except KeyError:
            points.append(project_points[str(default_point)]["name"])
    return points

def us_points_by_role_whith_names(us, project, roles):
    # FIXME: Improvement, get project_points from a project constant
    # FIXME: Improvement, get rolesofrom a project constant
    us_points = us.get("points", [])
    project_points = {str(p["id"]): p for p in project["points"]}
    default_point = project["default_points"]

    points = []
    for role in roles:
        try:
            points.append((role["name"], project_points[str(us_points[str(role["id"])])]["name"]))
        except KeyError:
            points.append((role["name"], project_points[str(default_point)]["name"]))
    return points

def issue_types(project):
    dc = {str(p["id"]): p for p in project.get("issue_types", [])}
    return OrderedDict(sorted(dc.items(), key=lambda t: t[1]["order"]))

def issue_statuses(project):
    dc = {str(p["id"]): p for p in project.get("issue_statuses", [])}
    return OrderedDict(sorted(dc.items(), key=lambda t: t[1]["order"]))

def priorities(project):
    dc = {str(p["id"]): p for p in project.get("priorities", [])}
    return OrderedDict(sorted(dc.items(), key=lambda t: t[1]["order"]))

def severities(project):
    dc = {str(p["id"]): p for p in project.get("severities", [])}
    return OrderedDict(sorted(dc.items(), key=lambda t: t[1]["order"]))


# Issues

def total_issues(issues_stats):
    return issues_stats.get("total_issues", 0)

def opened_issues(issues_stats):
    return issues_stats.get("opened_issues", 0)

def closed_issues(issues_stats):
    return issues_stats.get("closed_issues", 0)

def issues_statuses_stats(issues_stats):
    return issues_stats.get("issues_per_status", {})

def issues_priorities_stats(issues_stats):
    return issues_stats.get("issues_per_priority", {})

def issues_severities_stats(issues_stats):
    return issues_stats.get("issues_per_severity", {})

def issue_ref(issue):
    return issue.get("ref", "--")

def issue_subject(issue):
    return issue.get("subject", "------")

def issue_status_with_color(issue, project, default_color="#ffffff"):
    # FIXME: Improvement, get issues_statuses from a project constant
    # TODO: Check that the color is in hex format
    status_id = issue.get("status", None)
    if status_id:
        issue_statuses = {str(p["id"]): p for p in project["issue_statuses"]}
        try:
            return (issue_statuses[str(status_id)]["color"] or default_color,
                    issue_statuses[str(status_id)]["name"])
        except KeyError:
            pass
    return (default_color, "---")

def issue_priority_with_color(issue, project, default_color="#ffffff"):
    # FIXME: Improvement, get priorities from a project constant
    # TODO: Check that the color is in hex format
    priority_id = issue.get("priority", None)
    if priority_id:
        priorities = {str(p["id"]): p for p in project["priorities"]}
        try:
            return (priorities[str(priority_id)]["color"] or default_color,
                    priorities[str(priority_id)]["name"])
        except KeyError:
            pass
    return (default_color, "---")

def issue_severity_with_color(issue, project, default_color="#ffffff"):
    # FIXME: Improvement, get severities from a project constant
    # TODO: Check that the color is in hex format
    severity_id = issue.get("severity", None)
    if severity_id:
        severities = {str(p["id"]): p for p in project["severities"]}
        try:
            return (severities[str(severity_id)]["color"] or default_color,
                    severities[str(severity_id)]["name"])
        except KeyError:
            pass
    return (default_color, "---")

def issue_assigned_to_with_color(issue, project, default_color="#ffffff"):
    # FIXME: Improvement, get memberships and users from a project constant
    # TODO: Check that the color is in hex format
    user_id = issue.get("assigned_to", None)
    if user_id:
        memberships = {str(p["user"]): p for p in project["memberships"]}
        try:
            return (memberships[str(user_id)]["color"] or default_color,
                    memberships[str(user_id)]["full_name"])
        except KeyError:
            pass
    return  (default_color, "Unassigned")

# Milestone

def milestone_name(milestone):
    return milestone.get("name", "------")

def milestone_total_points(milestone_stats):
    return sum(milestone_stats.get("total_points", {}).values())

def milestone_completed_points(milestone_stats):
    return sum(milestone_stats["completed_points"])

def milestone_closed_points(milestone):
    return sum(milestone["closed_points"].values())

def milestone_total_tasks(milestone_stats):
    return milestone_stats["total_tasks"]

def milestone_completed_tasks(milestone_stats):
    return milestone_stats["completed_tasks"]

def milestone_estimated_start(milestone_stats):
    return milestone_stats["estimated_start"]

def milestone_finish_date(milestone):
    return milestone["finish_date"]

def milestone_estimated_finish(milestone_stats):
    return milestone_stats["estimated_finish"]

def milestone_remaining_days(milestone_stats):
   return (date(milestone_stats["estimated_finish"]) - datetime.now()).days + 1

# Tasks

def task_ref(task):
    return task.get("ref", "--")

def task_subject(task):
    return task.get("subject", "------")

def task_finished_date(task):
    return task.get("finished_date", None)

def task_assigned_to_with_color(task, project, default_color="#ffffff"):
    # FIXME: Improvement, get memberships and users from a project constant
    # TODO: Check that the color is in hex format
    user_id = task.get("assigned_to", None)
    if user_id:
        memberships = {str(p["user"]): p for p in project["memberships"]}
        try:
            return (memberships[str(user_id)]["color"] or default_color,
                    memberships[str(user_id)]["full_name"])
        except KeyError:
            pass
    return  (default_color, "Unassigned")

def task_status_with_color(task, project, default_color="#ffffff"):
    # FIXME: Improvement, get tasks_statuses from a project constant
    # TODO: Check that the color is in hex format
    status_id = task.get("status", None)
    if status_id:
        task_statuses = {str(p["id"]): p for p in project["task_statuses"]}
        try:
            return (task_statuses[str(status_id)]["color"] or default_color,
                    task_statuses[str(status_id)]["name"])
        except KeyError:
            pass
    return (default_color, "---")

def tasks_per_user_story(tasks, user_story):
    return [t for t in tasks if t["user_story"] == user_story["id"]]

def unassigned_tasks(tasks):
    return [t for t in tasks if t["user_story"] == None]


# Wiki page

def slug(wiki_page):
    return wiki_page.get("slug", "")

def content(wiki_page):
    return wiki_page.get("content", "")

# Misc

def date(text, date_format="%Y-%m-%d"):
    return datetime.strptime(text, date_format)
