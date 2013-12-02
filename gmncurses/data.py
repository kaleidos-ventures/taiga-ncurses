# -*- coding: utf-8 -*-

"""
gmncurses.data
~~~~~~~~~~~~~~
"""

from datetime import datetime


def total_points(project_stats):
    return project_stats.get("total_points", 0)

def total_sprints(project_stats):
    return project_stats.get("total_milestones", 0)

def closed_points(project_stats):
    return  project_stats.get("closed_points", 0)

def closed_points_percentage(project_stats):
    try:
        return closed_points(project_stats) * 100 / total_points(project_stats)
    except ZeroDivisionError:
        return 0

def completed_sprints(project):
    milestones = project.get("list_of_milestones", [])
    now = datetime.now()
    return [m for m in milestones if date(m["finish_date"]) < now]

def date(text, date_format="%Y-%m-%d"):
    return datetime.strptime(text, date_format)

def defined_points(project_stats):
    return project_stats.get("defined_points", 0)

def defined_points_percentage(project_stats):
    try:
        return defined_points(project_stats) * 100 / total_points(project_stats)
    except ZeroDivisionError:
        return 0

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

def computable_roles(project):
    # FIXME
    return [r for r in project["roles"] if r["computable"]] if "roles" in project else []

def us_ref(us):
    return us.get("ref", "--")

def us_subject(us):
    return us.get("subject", "------")

def us_points_by_role(us, project, roles):
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

def us_total_points(us):
    return us.get("total_points", "--")
