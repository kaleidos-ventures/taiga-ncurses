# -*- coding: utf-8 -*-

"""
gmncurses.data
~~~~~~~~~~~~~~
"""

from datetime import datetime


# project_stats - Points

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

def closed_points_percentage(project_stats):
    try:
        return closed_points(project_stats) * 100 / total_points(project_stats)
    except ZeroDivisionError:
        return 0

def doomline_limit_points(project_stats):
    return total_points(project_stats) - assigned_points(project_stats)


# project_stats - Sprints

def total_sprints(project_stats):
    return project_stats.get("total_milestones", 0)

def completed_sprints(project):
    milestones = project.get("list_of_milestones", [])
    now = datetime.now()
    return [m for m in milestones if date(m["finish_date"]) < now]


# project - Sprints

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

# project - Roles

def computable_roles(project):
    # FIXME
    return [r for r in project["roles"] if r["computable"]] if "roles" in project else []


# User Stories data

def us_ref(us):
    return us.get("ref", "--")

def us_subject(us):
    return us.get("subject", "------")

def us_total_points(us):
    return us.get("total_points", "--")


# us, project, computable roles - US points

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


# issues stats - issues

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


# issue - issues

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
        return str(status)
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


# wiki_page - Wiki page

def slug(wiki_page):
    return wiki_page.get("slug", "")

def content(wiki_page):
    return wiki_page.get("content", "")

# Misc

def date(text, date_format="%Y-%m-%d"):
    return datetime.strptime(text, date_format)
