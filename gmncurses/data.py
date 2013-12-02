# -*- coding: utf-8 -*-

"""
gmncurses.data
~~~~~~~~~~~~~~
"""


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
    return len([m for m in milestones if m["closed"]])

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

def us_ref(us):
    return us.get("ref", "--")

def us_subject(us):
    return us.get("subject", "------")

def us_ux_points(us):
    # FIXME
    return 42

def us_design_points(us):
    # FIXME
    return 42

def us_front_points(us):
    pass
    # FIXME
    return 42

def us_back_points(us):
    # FIXME
    return 42
