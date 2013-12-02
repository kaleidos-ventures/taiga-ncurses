# -*- coding: utf-8 -*-

PROJECT = """
{
    "tags": "",
    "list_of_milestones": [],
    "memberships": [],
    "us_statuses": [
        {
            "id": 5,
            "name": "Open",
            "order": 1,
            "is_closed": false,
            "project": 3
        },
        {
            "id": 6,
            "name": "Closed",
            "order": 2,
            "is_closed": true,
            "project": 3
        }
    ],
    "points": [
        {
            "id": 25,
            "name": "?",
            "order": 1,
            "value": null,
            "project": 3
        },
        {
            "id": 26,
            "name": "0",
            "order": 2,
            "value": 0.0,
            "project": 3
        },
        {
            "id": 27,
            "name": "1/2",
            "order": 3,
            "value": 0.5,
            "project": 3
        },
        {
            "id": 28,
            "name": "1",
            "order": 4,
            "value": 1.0,
            "project": 3
        },
        {
            "id": 29,
            "name": "2",
            "order": 5,
            "value": 2.0,
            "project": 3
        },
        {
            "id": 30,
            "name": "3",
            "order": 6,
            "value": 3.0,
            "project": 3
        },
        {
            "id": 31,
            "name": "5",
            "order": 7,
            "value": 5.0,
            "project": 3
        },
        {
            "id": 32,
            "name": "8",
            "order": 8,
            "value": 8.0,
            "project": 3
        },
        {
            "id": 33,
            "name": "10",
            "order": 9,
            "value": 10.0,
            "project": 3
        },
        {
            "id": 34,
            "name": "15",
            "order": 10,
            "value": 15.0,
            "project": 3
        },
        {
            "id": 35,
            "name": "20",
            "order": 11,
            "value": 20.0,
            "project": 3
        },
        {
            "id": 36,
            "name": "40",
            "order": 12,
            "value": 40.0,
            "project": 3
        }
    ],
    "task_statuses": [
        {
            "id": 11,
            "name": "New",
            "order": 1,
            "is_closed": false,
            "color": "#999999",
            "project": 3
        },
        {
            "id": 12,
            "name": "In progress",
            "order": 2,
            "is_closed": false,
            "color": "#ff9900",
            "project": 3
        },
        {
            "id": 13,
            "name": "Ready for test",
            "order": 3,
            "is_closed": true,
            "color": "#ffcc00",
            "project": 3
        },
        {
            "id": 14,
            "name": "Closed",
            "order": 4,
            "is_closed": true,
            "color": "#669900",
            "project": 3
        },
        {
            "id": 15,
            "name": "Needs Info",
            "order": 5,
            "is_closed": false,
            "color": "#999999",
            "project": 3
        }
    ],
    "priorities": [
        {
            "id": 7,
            "name": "Low",
            "order": 1,
            "color": "#666666",
            "project": 3
        },
        {
            "id": 8,
            "name": "Normal",
            "order": 3,
            "color": "#669933",
            "project": 3
        },
        {
            "id": 9,
            "name": "High",
            "order": 5,
            "color": "#CC0000",
            "project": 3
        }
    ],
    "severities": [
        {
            "id": 11,
            "name": "Wishlist",
            "order": 1,
            "color": "#666666",
            "project": 3
        },
        {
            "id": 12,
            "name": "Minor",
            "order": 2,
            "color": "#669933",
            "project": 3
        },
        {
            "id": 13,
            "name": "Normal",
            "order": 3,
            "color": "blue",
            "project": 3
        },
        {
            "id": 14,
            "name": "Important",
            "order": 4,
            "color": "orange",
            "project": 3
        },
        {
            "id": 15,
            "name": "Critical",
            "order": 5,
            "color": "#CC0000",
            "project": 3
        }
    ],
    "issue_statuses": [
        {
            "id": 15,
            "name": "New",
            "order": 1,
            "is_closed": false,
            "color": "#8C2318",
            "project": 3
        },
        {
            "id": 16,
            "name": "In progress",
            "order": 2,
            "is_closed": false,
            "color": "#5E8C6A",
            "project": 3
        },
        {
            "id": 17,
            "name": "Ready for test",
            "order": 3,
            "is_closed": true,
            "color": "#88A65E",
            "project": 3
        },
        {
            "id": 18,
            "name": "Closed",
            "order": 4,
            "is_closed": true,
            "color": "#BFB35A",
            "project": 3
        },
        {
            "id": 19,
            "name": "Needs Info",
            "order": 5,
            "is_closed": false,
            "color": "#89BAB4",
            "project": 3
        },
        {
            "id": 20,
            "name": "Rejected",
            "order": 6,
            "is_closed": true,
            "color": "#CC0000",
            "project": 3
        },
        {
            "id": 21,
            "name": "Postponed",
            "order": 7,
            "is_closed": false,
            "color": "#666666",
            "project": 3
        }
    ],
    "issue_types": [
        {
            "id": 3,
            "name": "Bug",
            "order": 1,
            "color": "#89BAB4",
            "project": 3
        }
    ],
    "id": 3,
    "name": "Bar",
    "slug": "bar",
    "description": "asdf",
    "created_date": "2013-11-30T11:31:46.970Z",
    "modified_date": "2013-11-30T11:31:46.990Z",
    "owner": 1,
    "public": true,
    "total_milestones": 0,
    "total_story_points": 123.0,
    "default_points": 25,
    "default_us_status": 5,
    "default_task_status": 11,
    "default_priority": 8,
    "default_severity": 13,
    "default_issue_status": 15,
    "default_issue_type": 3,
    "default_question_status": 7,
    "members": []
}
"""

PROJECTS = """
[
    {
        "tags": "",
        "id": 3,
        "name": "Bar",
        "slug": "bar",
        "description": "asdf",
        "created_date": "2013-11-30T11:31:46.970Z",
        "modified_date": "2013-11-30T11:31:46.990Z",
        "owner": 1,
        "public": true,
        "total_milestones": 0,
        "total_story_points": 123.0,
        "default_points": 25,
        "default_us_status": 5,
        "default_task_status": 11,
        "default_priority": 8,
        "default_severity": 13,
        "default_issue_status": 15,
        "default_issue_type": 3,
        "default_question_status": 7,
        "members": []
    },
    {
        "tags": "",
        "id": 2,
        "name": "Foo",
        "slug": "foo",
        "description": "a",
        "created_date": "2013-11-30T11:31:28.339Z",
        "modified_date": "2013-11-30T11:31:28.358Z",
        "owner": 1,
        "public": true,
        "total_milestones": 0,
        "total_story_points": 6.0,
        "default_points": 13,
        "default_us_status": 3,
        "default_task_status": 6,
        "default_priority": 5,
        "default_severity": 8,
        "default_issue_status": 8,
        "default_issue_type": 2,
        "default_question_status": 4,
        "members": []
    }
]
"""

USER_STORIES = """
[]
"""

PROJECT_STATS = """
{
    "milestones": [
        {
            "optimal": 123.0, 
            "evolution": 123.0, 
            "client-increment": 0, 
            "name": "Sprint 1", 
            "team-increment": 0
        }, 
        {
            "optimal": 0.0, 
            "evolution": 123.0, 
            "client-increment": 0, 
            "name": "Project End", 
            "team-increment": 0
        }
    ], 
    "defined_points": 0, 
    "closed_points": 0, 
    "total_points": 123.0, 
    "total_milestones": 1, 
    "assigned_points": 0, 
    "name": "Bar"
}

"""
