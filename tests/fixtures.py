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
[
    {
        "tags": [
            "ipsam",
            "voluptatum",
            "accusantium"
        ],
        "points": {
            "4": 3,
            "1": 1,
            "3": 12,
            "2": 3
        },
        "total_points": 41.0,
        "comment": "",
        "id": 20,
        "ref": 21,
        "milestone": null,
        "project": 1,
        "owner": 8,
        "status": 1,
        "is_closed": false,
        "order": 1,
        "created_date": "2013-12-20T09:53:55.488Z",
        "modified_date": "2013-12-20T09:53:55.488Z",
        "finish_date": null,
        "subject": "Feature/improved image admin",
        "description": "Assumenda harum nisi, quibusdam fugit distinctio assumenda.",
        "client_requirement": false,
        "team_requirement": false,
        "watchers": []
    },
    {
        "tags": [
            "non",
            "earum"
        ],
        "points": {
            "4": 9,
            "1": 6,
            "3": 9,
            "2": 5
        },
        "total_points": 25.0,
        "comment": "",
        "id": 30,
        "ref": 31,
        "milestone": null,
        "project": 1,
        "owner": 2,
        "status": 1,
        "is_closed": false,
        "order": 2,
        "created_date": "2013-12-20T09:53:57.189Z",
        "modified_date": "2013-12-20T09:53:57.189Z",
        "finish_date": null,
        "subject": "Lighttpd support",
        "description": "Eius mollitia aperiam quia amet atque recusandae eaque cumque facilis, laborum rem magni voluptatum eveniet recusandae odit reprehenderit, est enim adipisci. Reiciendis id aperiam, ipsam et quas hic est in, saepe enim nulla tempore, dignissimos doloremque blanditiis est quisquam odio dolore saepe iure quia ad, magnam amet consequatur odit? Tempora minima nostrum repellat eos nesciunt aperiam placeat cupiditate quos quidem dolore, totam est blanditiis, ea adipisci fugiat voluptates aliquam, soluta consectetur similique officiis placeat sint explicabo minus molestias? Corporis molestias eveniet porro reprehenderit inventore ducimus a architecto cum, saepe quae laboriosam, officiis vel itaque repudiandae aspernatur vero officia harum culpa?",
        "client_requirement": false,
        "team_requirement": false,
        "watchers": []
    },
    {
        "tags": [
            "nihil",
            "nulla",
            "perferendis"
        ],
        "points": {
            "4": 10,
            "1": 8,
            "3": 3,
            "2": 9
        },
        "total_points": 33.5,
        "comment": "",
        "id": 25,
        "ref": 26,
        "milestone": null,
        "project": 1,
        "owner": 9,
        "status": 1,
        "is_closed": false,
        "order": 3,
        "created_date": "2013-12-20T09:53:56.171Z",
        "modified_date": "2013-12-20T09:53:56.171Z",
        "finish_date": null,
        "subject": "Feature/improved image admin",
        "description": "Harum et odio a voluptate dignissimos optio doloribus pariatur eligendi voluptates, quis saepe commodi minus nulla dignissimos ad laboriosam, cum eos fuga consequatur quo totam, ex vitae delectus molestias deserunt exercitationem tenetur ipsum dolores quaerat reiciendis, earum eveniet veniam?",
        "client_requirement": false,
        "team_requirement": false,
        "watchers": []
    },
    {
        "tags": [
            "itaque"
        ],
        "points": {
            "4": 11,
            "1": 6,
            "3": 7,
            "2": 1
        },
        "total_points": 28.0,
        "comment": "",
        "id": 21,
        "ref": 22,
        "milestone": null,
        "project": 1,
        "owner": 8,
        "status": 1,
        "is_closed": false,
        "order": 4,
        "created_date": "2013-12-20T09:53:55.596Z",
        "modified_date": "2013-12-20T09:53:55.596Z",
        "finish_date": null,
        "subject": "Migrate to Python 3 and milk a beautiful cow",
        "description": "Quos molestias quam aut neque eaque fugiat fugit earum porro impedit veniam, ad nulla officiis accusamus voluptatum, ratione rem voluptatem natus nostrum?",
        "client_requirement": false,
        "team_requirement": false,
        "watchers": []
    },
    {
        "tags": [
            "ducimus"
        ],
        "points": {
            "4": 12,
            "1": 12,
            "3": 12,
            "2": 12
        },
        "total_points": 160.0,
        "comment": "",
        "id": 22,
        "ref": 23,
        "milestone": null,
        "project": 1,
        "owner": 5,
        "status": 1,
        "is_closed": false,
        "order": 5,
        "created_date": "2013-12-20T09:53:55.702Z",
        "modified_date": "2013-12-20T13:26:34.877Z",
        "finish_date": null,
        "subject": "Fixing templates for Django 1.6.",
        "description": "Fixing templates for Django 1.6.",
        "client_requirement": false,
        "team_requirement": false,
        "watchers": []
    },
    {
        "tags": [
            "corporis",
            "assumenda",
            "exercitationem"
        ],
        "points": {
            "4": 4,
            "1": 10,
            "3": 9,
            "2": 2
        },
        "total_points": 26.0,
        "comment": "",
        "id": 29,
        "ref": 30,
        "milestone": null,
        "project": 1,
        "owner": 8,
        "status": 1,
        "is_closed": false,
        "order": 7,
        "created_date": "2013-12-20T09:53:56.943Z",
        "modified_date": "2013-12-20T09:53:56.943Z",
        "finish_date": null,
        "subject": "Migrate to Python 3 and milk a beautiful cow",
        "description": "Delectus temporibus quam nesciunt explicabo aut? Molestiae soluta quo fuga nihil facere rem earum voluptatum, voluptates id quo voluptatibus cumque obcaecati repellendus, exercitationem pariatur facilis omnis, corrupti cum quaerat impedit? Qui voluptatem beatae modi odio, facilis reiciendis atque fugit alias, similique aliquid neque quia necessitatibus officiis ut adipisci, dolor dolores maxime non veritatis eveniet assumenda quos blanditiis.",
        "client_requirement": false,
        "team_requirement": false,
        "watchers": []
    },
    {
        "tags": [
            "dasds"
        ],
        "points": {
            "4": 5,
            "1": 7,
            "3": 7,
            "2": 5
        },
        "total_points": 14.0,
        "comment": "",
        "id": 113,
        "ref": 29,
        "milestone": null,
        "project": 1,
        "owner": 1,
        "status": 2,
        "is_closed": false,
        "order": 8,
        "created_date": "2013-12-20T13:26:06.988Z",
        "modified_date": "2013-12-26T17:30:21.328Z",
        "finish_date": null,
        "subject": "tyuiweryuirteyuirtweitweyrerteyu",
        "description": "tyuiweryuirteyuirtweitweyrerteyu",
        "client_requirement": true,
        "team_requirement": true,
        "watchers": []
    },
    {
        "tags": [
            "dicta",
            "cupiditate",
            "doloremque"
        ],
        "points": {
            "4": 11,
            "1": 12,
            "3": 9,
            "2": 8
        },
        "total_points": 78.0,
        "comment": "",
        "id": 24,
        "ref": 25,
        "milestone": null,
        "project": 1,
        "owner": 4,
        "status": 1,
        "is_closed": false,
        "order": 9,
        "created_date": "2013-12-20T09:53:55.976Z",
        "modified_date": "2013-12-20T09:53:55.976Z",
        "finish_date": null,
        "subject": "Fixing templates for Django 1.6.",
        "description": "Quidem cumque doloribus, quod assumenda beatae inventore optio enim, voluptate architecto aliquam ullam fugiat, temporibus eos iure voluptatum at ab?",
        "client_requirement": false,
        "team_requirement": false,
        "watchers": []
    },
    {
        "tags": [
            "omnis",
            "saepe"
        ],
        "points": {
            "4": 9,
            "1": 6,
            "3": 4,
            "2": 3
        },
        "total_points": 14.5,
        "comment": "",
        "id": 26,
        "ref": 27,
        "milestone": null,
        "project": 1,
        "owner": 2,
        "status": 1,
        "is_closed": false,
        "order": 11,
        "created_date": "2013-12-20T09:53:56.319Z",
        "modified_date": "2013-12-20T09:53:56.319Z",
        "finish_date": null,
        "subject": "Support for bulk actions",
        "description": "Placeat provident aspernatur nemo recusandae tenetur, veritatis nam quod nihil repellat vel nisi minus labore beatae, itaque quaerat id pariatur laborum, et eius harum excepturi eligendi omnis sit inventore delectus aliquid impedit, deleniti soluta mollitia distinctio inventore. Voluptatibus rerum eveniet quo similique possimus facilis nulla aspernatur, tenetur aspernatur excepturi, ab commodi quos rerum totam illo.",
        "client_requirement": false,
        "team_requirement": false,
        "watchers": []
    },
    {
        "tags": [
            "ipsam",
            "aspernatur",
            "inventore"
        ],
        "points": {
            "4": 1,
            "1": 9,
            "3": 5,
            "2": 11
        },
        "total_points": 32.0,
        "comment": "",
        "id": 27,
        "ref": 28,
        "milestone": null,
        "project": 1,
        "owner": 5,
        "status": 1,
        "is_closed": false,
        "order": 12,
        "created_date": "2013-12-20T09:53:56.516Z",
        "modified_date": "2013-12-20T09:53:56.516Z",
        "finish_date": null,
        "subject": "Create testsuite with matrix builds",
        "description": "Quasi placeat maxime recusandae quo obcaecati quisquam distinctio eius, porro cumque at excepturi sunt? Laborum ut non placeat neque doloribus delectus animi. Dolore atque a rem necessitatibus culpa veritatis consequuntur ex repellat dolorem itaque, facere dolore neque id placeat in voluptatem, eaque accusantium nostrum ipsum error perferendis repellendus, assumenda quas non neque tempore sunt voluptate ullam veritatis velit reprehenderit, mollitia laudantium fugiat earum ad perferendis ipsa voluptatibus minus distinctio? Unde magni placeat dolorum corporis sequi, rerum beatae atque laborum officiis deserunt doloribus, odio provident non doloremque unde totam dicta voluptates.",
        "client_requirement": false,
        "team_requirement": false,
        "watchers": []
    },
    {
        "tags": [
            "laudantium"
        ],
        "points": {
            "4": 8,
            "1": 4,
            "3": 2,
            "2": 10
        },
        "total_points": 24.0,
        "comment": "",
        "id": 31,
        "ref": 32,
        "milestone": null,
        "project": 1,
        "owner": 9,
        "status": 1,
        "is_closed": false,
        "order": 13,
        "created_date": "2013-12-20T09:53:57.356Z",
        "modified_date": "2013-12-20T09:53:57.356Z",
        "finish_date": null,
        "subject": "Experimental: modular file types",
        "description": "Suscipit nulla eos veniam earum. Unde cum excepturi aliquam est facere suscipit nemo, itaque ut vitae temporibus illum a nisi ipsam eius earum, perferendis nesciunt non voluptates quae quidem doloribus soluta assumenda omnis, vitae sed ipsum nam officiis adipisci nesciunt. Fuga alias accusantium at ducimus distinctio ipsum beatae? Obcaecati assumenda quos a sequi voluptatum aut, nam voluptate ea similique doloribus error, tempora qui molestiae ut earum possimus reiciendis cumque sint, optio distinctio quis odit delectus ab enim iure eaque iusto, voluptate tenetur fugit commodi omnis officia?",
        "client_requirement": false,
        "team_requirement": false,
        "watchers": []
    },
    {
        "tags": [
            "consequatur",
            "dolor",
            "fugiat"
        ],
        "points": {
            "4": 3,
            "1": 5,
            "3": 1,
            "2": 1
        },
        "total_points": 2.5,
        "comment": "",
        "id": 32,
        "ref": 33,
        "milestone": null,
        "project": 1,
        "owner": 3,
        "status": 1,
        "is_closed": false,
        "order": 14,
        "created_date": "2013-12-20T09:53:57.548Z",
        "modified_date": "2013-12-20T09:53:57.548Z",
        "finish_date": null,
        "subject": "Experimental: modular file types",
        "description": "Ad ut suscipit iste dicta doloribus pariatur modi saepe corrupti, nemo odit sit voluptatem sed voluptates inventore architecto rerum, aspernatur cumque hic totam deleniti praesentium? Iusto earum minima aut illum ex dignissimos voluptatum enim adipisci molestias, rem eum deserunt modi iste, mollitia debitis ex possimus sapiente assumenda reiciendis hic nulla eveniet repellendus nihil? Ratione expedita consequatur commodi voluptates molestias nemo similique veniam atque possimus, debitis nostrum laboriosam temporibus minus nesciunt, ut quo nulla quos, vitae consequatur cum ex veniam repellat recusandae sint reiciendis aperiam, atque harum illo.",
        "client_requirement": false,
        "team_requirement": false,
        "watchers": []
    },
    {
        "tags": [
            "officiis",
            "magnam"
        ],
        "points": {
            "4": 8,
            "1": 5,
            "3": 12,
            "2": 7
        },
        "total_points": 55.0,
        "comment": "",
        "id": 36,
        "ref": 37,
        "milestone": null,
        "project": 1,
        "owner": 5,
        "status": 1,
        "is_closed": false,
        "order": 15,
        "created_date": "2013-12-20T09:53:58.363Z",
        "modified_date": "2013-12-20T09:53:58.363Z",
        "finish_date": null,
        "subject": "Experimental: modular file types",
        "description": "Corrupti illo dolorem iste amet excepturi necessitatibus dicta itaque, officia ipsam voluptatem molestiae aut quae rerum laborum provident nesciunt optio, iusto alias nostrum incidunt pariatur sunt quisquam, sit perferendis nisi? Explicabo aliquam nesciunt eius sint, voluptatibus aspernatur laborum eveniet voluptates quasi cupiditate voluptatum necessitatibus eligendi. Voluptate unde voluptates optio minima sint veniam ipsam, quod eaque consequatur ducimus quaerat nostrum vero impedit totam iure aliquid enim, possimus asperiores repellat dolore eos consequuntur enim reiciendis corrupti cupiditate eum, et ipsam sequi, iure aliquam unde modi recusandae temporibus expedita vitae nobis pariatur voluptatum aspernatur. Molestias aut architecto accusamus perferendis officiis alias ratione, itaque nemo quae voluptas eius officia modi voluptate ea quaerat deserunt, esse laudantium possimus expedita quos numquam atque, excepturi voluptatibus alias repellat omnis iste autem.",
        "client_requirement": false,
        "team_requirement": false,
        "watchers": []
    },
    {
        "tags": [
            "quae",
            "deserunt"
        ],
        "points": {
            "4": 11,
            "1": 3,
            "3": 7,
            "2": 3
        },
        "total_points": 26.0,
        "comment": "",
        "id": 33,
        "ref": 34,
        "milestone": null,
        "project": 1,
        "owner": 3,
        "status": 1,
        "is_closed": false,
        "order": 16,
        "created_date": "2013-12-20T09:53:57.761Z",
        "modified_date": "2013-12-20T09:53:57.761Z",
        "finish_date": null,
        "subject": "Added file copying and processing of images (resizing)",
        "description": "Blanditiis placeat quibusdam nobis beatae velit excepturi corrupti, accusamus nulla maiores? Sequi dicta maxime dolorem placeat laborum tenetur voluptatibus saepe omnis a officia, amet quam illo eaque maiores accusantium laudantium nemo error maxime fugit aspernatur, odit veritatis repellat, perferendis tenetur rerum minus, tempore itaque et minima ducimus pariatur illum temporibus deserunt? Quod possimus ab minus reprehenderit beatae ipsum eveniet, recusandae doloremque modi.",
        "client_requirement": false,
        "team_requirement": false,
        "watchers": []
    },
    {
        "tags": [
            "debitis",
            "odit"
        ],
        "points": {
            "4": 5,
            "1": 4,
            "3": 7,
            "2": 3
        },
        "total_points": 8.5,
        "comment": "",
        "id": 34,
        "ref": 35,
        "milestone": null,
        "project": 1,
        "owner": 9,
        "status": 1,
        "is_closed": false,
        "order": 17,
        "created_date": "2013-12-20T09:53:57.940Z",
        "modified_date": "2013-12-20T09:53:57.940Z",
        "finish_date": null,
        "subject": "Support for bulk actions",
        "description": "Officia maxime vero enim esse non, sint nemo maxime repudiandae eos consectetur vitae omnis placeat impedit, suscipit voluptas laborum recusandae porro animi qui temporibus fugiat, velit tenetur ducimus neque? Vel quibusdam nobis iste atque ipsum, omnis recusandae labore fuga amet quas facilis sit adipisci consectetur excepturi nesciunt, iusto molestias eius placeat odit nostrum rerum temporibus eveniet voluptates laboriosam, deserunt quibusdam laborum ipsum quia, quae aliquam assumenda eius corporis quod recusandae excepturi quidem voluptates. Reprehenderit quod rerum facilis inventore tempore ullam, ipsam a aliquam totam reprehenderit.",
        "client_requirement": false,
        "team_requirement": false,
        "watchers": []
    },
    {
        "tags": [
            "voluptates",
            "maiores"
        ],
        "points": {
            "4": 9,
            "1": 1,
            "3": 6,
            "2": 11
        },
        "total_points": 33.0,
        "comment": "",
        "id": 35,
        "ref": 36,
        "milestone": null,
        "project": 1,
        "owner": 11,
        "status": 1,
        "is_closed": false,
        "order": 18,
        "created_date": "2013-12-20T09:53:58.099Z",
        "modified_date": "2013-12-20T09:53:58.099Z",
        "finish_date": null,
        "subject": "Experimental: modular file types",
        "description": "A voluptate saepe praesentium voluptatum ducimus, tempore consequatur esse beatae nihil, ratione recusandae quibusdam, necessitatibus et perspiciatis nam repellendus neque quasi distinctio. Rem autem recusandae facere.",
        "client_requirement": false,
        "team_requirement": false,
        "watchers": []
    }
]
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

PROJECT_ISSUES_STATS = """
{
    "issues_per_owner": {
        "1": {
            "count": 2,
            "name": "admin",
            "color": "",
            "username": "admin",
            "id": 1
        },
        "2": {
            "count": 2,
            "name": "Marina Medina",
            "color": "#FFFF00",
            "username": "user-0",
            "id": 2
        },
        "3": {
            "count": 1,
            "name": "Purificacion Montero",
            "color": "#FC8EAC",
            "username": "user-1",
            "id": 3
        },
        "4": {
            "count": 1,
            "name": "Eugenio Herrera",
            "color": "#FFFF00",
            "username": "user-2",
            "id": 4
        },
        "5": {
            "count": 1,
            "name": "Carolina Mora",
            "color": "#FC8EAC",
            "username": "user-3",
            "id": 5
        },
        "7": {
            "count": 2,
            "name": "Aurora Calvo",
            "color": "#4B0082",
            "username": "user-5",
            "id": 7
        },
        "8": {
            "count": 3,
            "name": "Susana Reyes",
            "color": "#FC8EAC",
            "username": "user-6",
            "id": 8
        },
        "9": {
            "count": 2,
            "name": "Josefina Reyes",
            "color": "#FFFF00",
            "username": "user-7",
            "id": 9
        },
        "10": {
            "count": 4,
            "name": "Victoria Nu\u00f1ez",
            "color": "#FFF8E7",
            "username": "user-8",
            "id": 10
        },
        "11": {
            "count": 2,
            "name": "Teresa Gallardo",
            "color": "#FFCC00",
            "username": "user-9",
            "id": 11
        }
    },
    "closed_issues": 6,
    "issues_per_type": {
        "1": {
            "count": 20,
            "name": "Bug",
            "color": "#89BAB4",
            "id": 1
        }
    },
    "total_issues": 20,
    "last_four_weeks_days": {
        "by_priority": {
            "1": {
                "name": "Low",
                "data": [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3
                ],
                "color": "#666666",
                "id": 1
            },
            "2": {
                "name": "Normal",
                "data": [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    6,
                    4,
                    4,
                    4,
                    4,
                    4,
                    4,
                    4,
                    4
                ],
                "color": "#669933",
                "id": 2
            },
            "3": {
                "name": "High",
                "data": [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    11,
                    7,
                    7,
                    7,
                    7,
                    7,
                    7,
                    7,
                    7
                ],
                "color": "#CC0000",
                "id": 3
            }
        },
        "by_open_closed": {
            "closed": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                6,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
            ],
            "open": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                20,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
            ]
        },
        "by_severity": {
            "1": {
                "name": "Wishlist",
                "data": [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    3,
                    2,
                    2,
                    2,
                    2,
                    2,
                    2,
                    2,
                    2
                ],
                "color": "#666666",
                "id": 1
            },
            "2": {
                "name": "Minor",
                "data": [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    7,
                    5,
                    5,
                    5,
                    5,
                    5,
                    5,
                    5,
                    5
                ],
                "color": "#669933",
                "id": 2
            },
            "3": {
                "name": "Normal",
                "data": [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    6,
                    5,
                    5,
                    5,
                    5,
                    5,
                    5,
                    5,
                    5
                ],
                "color": "#0000FF",
                "id": 3
            },
            "4": {
                "name": "Important",
                "data": [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    3,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1
                ],
                "color": "#FFA500",
                "id": 4
            },
            "5": {
                "name": "Critical",
                "data": [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1
                ],
                "color": "#CC0000",
                "id": 5
            }
        },
        "by_status": {}
    },
    "opened_issues": 14,
    "issues_per_priority": {
        "1": {
            "count": 3,
            "name": "Low",
            "color": "#666666",
            "id": 1
        },
        "2": {
            "count": 6,
            "name": "Normal",
            "color": "#669933",
            "id": 2
        },
        "3": {
            "count": 11,
            "name": "High",
            "color": "#CC0000",
            "id": 3
        }
    },
    "issues_per_status": {
        "1": {
            "count": 1,
            "name": "New",
            "color": "#8C2318",
            "id": 1
        },
        "2": {
            "count": 4,
            "name": "In progress",
            "color": "#5E8C6A",
            "id": 2
        },
        "3": {
            "count": 1,
            "name": "Ready for test",
            "color": "#88A65E",
            "id": 3
        },
        "4": {
            "count": 1,
            "name": "Closed",
            "color": "#BFB35A",
            "id": 4
        },
        "5": {
            "count": 5,
            "name": "Needs Info",
            "color": "#89BAB4",
            "id": 5
        },
        "6": {
            "count": 4,
            "name": "Rejected",
            "color": "#CC0000",
            "id": 6
        },
        "7": {
            "count": 4,
            "name": "Postponed",
            "color": "#666666",
            "id": 7
        }
    },
    "issues_per_assigned_to": {
        "0": {
            "count": 1,
            "name": "Unassigned",
            "color": "black",
            "username": "Unassigned",
            "id": 0
        },
        "1": {
            "count": 2,
            "name": "admin",
            "color": "",
            "username": "admin",
            "id": 1
        },
        "2": {
            "count": 4,
            "name": "Marina Medina",
            "color": "#FFFF00",
            "username": "user-0",
            "id": 2
        },
        "3": {
            "count": 2,
            "name": "Purificacion Montero",
            "color": "#FC8EAC",
            "username": "user-1",
            "id": 3
        },
        "4": {
            "count": 1,
            "name": "Eugenio Herrera",
            "color": "#FFFF00",
            "username": "user-2",
            "id": 4
        },
        "5": {
            "count": 1,
            "name": "Carolina Mora",
            "color": "#FC8EAC",
            "username": "user-3",
            "id": 5
        },
        "7": {
            "count": 3,
            "name": "Aurora Calvo",
            "color": "#4B0082",
            "username": "user-5",
            "id": 7
        },
        "9": {
            "count": 2,
            "name": "Josefina Reyes",
            "color": "#FFFF00",
            "username": "user-7",
            "id": 9
        },
        "10": {
            "count": 4,
            "name": "Victoria Nu\u00f1ez",
            "color": "#FFF8E7",
            "username": "user-8",
            "id": 10
        }
    },
    "issues_per_severity": {
        "1": {
            "count": 3,
            "name": "Wishlist",
            "color": "#666666",
            "id": 1
        },
        "2": {
            "count": 7,
            "name": "Minor",
            "color": "#669933",
            "id": 2
        },
        "3": {
            "count": 6,
            "name": "Normal",
            "color": "#0000FF",
            "id": 3
        },
        "4": {
            "count": 3,
            "name": "Important",
            "color": "#FFA500",
            "id": 4
        },
        "5": {
            "count": 1,
            "name": "Critical",
            "color": "#CC0000",
            "id": 5
        }
    }
}
"""

ISSUES = """
[
    {
        "tags": [
            "ratione",
            "omnis",
            "saepe",
            "tempora",
            "repellat"
        ],
        "comment": "",
        "is_closed": false,
        "id": 1,
        "ref": 2,
        "owner": 2,
        "status": 7,
        "severity": 5,
        "priority": 2,
        "type": 1,
        "milestone": null,
        "project": 1,
        "created_date": "2013-12-20T09:53:59.044Z",
        "modified_date": "2013-12-20T09:53:59.609Z",
        "finished_date": null,
        "subject": "Implement the form",
        "description": "Alias voluptatem nulla quo reiciendis dicta distinctio, quis vel facilis quae dolore rerum earum error nesciunt, ipsam itaque eius placeat doloribus voluptate sequi? Impedit iure adipisci et itaque debitis nihil vel ipsum esse ut perspiciatis. Facilis fuga exercitationem illo ipsam eveniet, tempora assumenda voluptate, tenetur saepe doloribus beatae neque quae quasi culpa reprehenderit et, totam temporibus deleniti consectetur rerum quis eaque commodi.",
        "assigned_to": 1,
        "watchers": []
    },
    {
        "tags": [
            "dolores",
            "odio",
            "reiciendis"
        ],
        "comment": "",
        "is_closed": false,
        "id": 2,
        "ref": 3,
        "owner": 9,
        "status": 2,
        "severity": 1,
        "priority": 3,
        "type": 1,
        "milestone": null,
        "project": 1,
        "created_date": "2013-12-20T09:53:59.624Z",
        "modified_date": "2013-12-20T09:53:59.756Z",
        "finished_date": null,
        "subject": "Lighttpd x-sendfile support",
        "description": "Cumque voluptas error vitae cupiditate doloribus dolorem at eveniet. Fugiat inventore doloremque provident dolorem ipsum itaque ex et, facilis sint tempore fuga exercitationem dolores quas aliquid ad, laudantium voluptate nesciunt debitis.",
        "assigned_to": 2,
        "watchers": []
    },
    {
        "tags": [
            "iure",
            "non",
            "vel"
        ],
        "comment": "",
        "is_closed": true,
        "id": 3,
        "ref": 4,
        "owner": 7,
        "status": 4,
        "severity": 4,
        "priority": 2,
        "type": 1,
        "milestone": null,
        "project": 1,
        "created_date": "2013-12-20T09:53:59.771Z",
        "modified_date": "2013-12-20T09:53:59.795Z",
        "finished_date": "2013-12-20T09:53:59.768Z",
        "subject": "Create the user model",
        "description": "Fugiat mollitia cum nam rerum odio?",
        "assigned_to": 3,
        "watchers": []
    },
    {
        "tags": [
            "reiciendis",
            "maiores",
            "adipisci"
        ],
        "comment": "",
        "is_closed": true,
        "id": 4,
        "ref": 5,
        "owner": 2,
        "status": 6,
        "severity": 3,
        "priority": 2,
        "type": 1,
        "milestone": null,
        "project": 1,
        "created_date": "2013-12-20T09:53:59.810Z",
        "modified_date": "2013-12-20T09:53:59.906Z",
        "finished_date": "2013-12-20T09:53:59.807Z",
        "subject": "Migrate to Python 3 and milk a beautiful cow",
        "description": "Ad eaque nostrum ab officiis consequuntur nesciunt fuga, minus ex commodi repellat accusamus libero cupiditate esse, illum accusamus exercitationem hic repudiandae sed reprehenderit tempore architecto dignissimos. Non est minus asperiores, enim provident debitis facilis, veniam corporis obcaecati laudantium quasi incidunt alias sit nemo iste culpa, consectetur ex dignissimos porro quae cum ipsa fugiat, nemo laboriosam eveniet a nihil vitae impedit culpa deleniti at ab quidem.",
        "assigned_to": 10,
        "watchers": []
    },
    {
        "tags": [
            "pariatur",
            "praesentium",
            "perspiciatis",
            "totam"
        ],
        "comment": "",
        "is_closed": true,
        "id": 5,
        "ref": 6,
        "owner": 5,
        "status": 6,
        "severity": 2,
        "priority": 3,
        "type": 1,
        "milestone": null,
        "project": 1,
        "created_date": "2013-12-20T09:53:59.920Z",
        "modified_date": "2013-12-20T09:54:00.012Z",
        "finished_date": "2013-12-20T09:53:59.917Z",
        "subject": "Lighttpd x-sendfile support",
        "description": "Molestias sit officia suscipit et officiis voluptas iste in deserunt, voluptate earum ad perferendis vel recusandae, porro sequi distinctio incidunt veritatis qui alias esse veniam?",
        "assigned_to": 3,
        "watchers": []
    },
    {
        "tags": [
            "aliquam",
            "magnam"
        ],
        "comment": "",
        "is_closed": true,
        "id": 6,
        "ref": 7,
        "owner": 8,
        "status": 6,
        "severity": 1,
        "priority": 3,
        "type": 1,
        "milestone": null,
        "project": 1,
        "created_date": "2013-12-20T09:54:00.025Z",
        "modified_date": "2013-12-20T09:54:00.051Z",
        "finished_date": "2013-12-20T09:54:00.022Z",
        "subject": "Add setting to allow regular users to create folders at the root level.",
        "description": "Et atque minus repellat maiores, debitis praesentium aperiam nihil suscipit eum, ipsa ut aliquid inventore? Maiores vitae maxime officia, tempore consequatur ipsam, vero vel quos neque asperiores consequuntur quibusdam suscipit, vero illo atque sapiente tenetur?",
        "assigned_to": 2,
        "watchers": []
    },
    {
        "tags": [
            "nisi",
            "blanditiis",
            "magni"
        ],
        "comment": "",
        "is_closed": false,
        "id": 7,
        "ref": 8,
        "owner": 11,
        "status": 7,
        "severity": 3,
        "priority": 3,
        "type": 1,
        "milestone": null,
        "project": 1,
        "created_date": "2013-12-20T09:54:00.065Z",
        "modified_date": "2013-12-20T09:54:00.114Z",
        "finished_date": null,
        "subject": "Feature/improved image admin",
        "description": "Recusandae in inventore aut quasi facere nemo, ut sed delectus rem tempore mollitia nemo, minima impedit debitis quam quae. Quos corrupti labore ea molestias error soluta nisi. Modi illum sunt voluptatibus, consequuntur ullam eligendi amet blanditiis non hic magnam, cumque eius et atque sed deserunt sunt veritatis provident harum qui, beatae enim ratione neque.",
        "assigned_to": 10,
        "watchers": []
    },
    {
        "tags": [
            "cupiditate",
            "alias",
            "pariatur",
            "cum"
        ],
        "comment": "",
        "is_closed": true,
        "id": 8,
        "ref": 9,
        "owner": 11,
        "status": 3,
        "severity": 4,
        "priority": 3,
        "type": 1,
        "milestone": null,
        "project": 1,
        "created_date": "2013-12-20T09:54:00.128Z",
        "modified_date": "2013-12-20T09:54:00.178Z",
        "finished_date": "2013-12-20T09:54:00.125Z",
        "subject": "get_actions() does not check for 'delete_selected' in actions",
        "description": "Assumenda eligendi veritatis magni nisi odit aliquam quibusdam excepturi maxime esse dolorum, dolorem perferendis facilis iure, ullam dolorum cupiditate dolore sunt voluptatem quae ea quidem dignissimos delectus, sequi a molestias accusantium tenetur alias voluptas beatae, veniam quia minima minus? Quis repellat nemo vero atque consequuntur illum neque deserunt corporis minus? Rerum dolore odio dicta porro possimus eum necessitatibus fuga maiores accusamus, odit libero aliquam distinctio, nemo culpa ex mollitia repudiandae sed aspernatur distinctio autem doloremque?",
        "assigned_to": 9,
        "watchers": []
    },
    {
        "tags": [
            "eos"
        ],
        "comment": "",
        "is_closed": false,
        "id": 9,
        "ref": 10,
        "owner": 10,
        "status": 2,
        "severity": 2,
        "priority": 1,
        "type": 1,
        "milestone": null,
        "project": 1,
        "created_date": "2013-12-20T09:54:00.193Z",
        "modified_date": "2013-12-20T09:54:00.197Z",
        "finished_date": null,
        "subject": "Add setting to allow regular users to create folders at the root level.",
        "description": "Nesciunt consequuntur dignissimos aut itaque ipsam natus accusamus possimus minima, eos temporibus ullam cumque voluptatem quas optio fugit assumenda laboriosam ab officiis, qui iusto fugit quos unde doloremque ipsum impedit odio incidunt totam culpa. Qui assumenda quasi eaque, quo aperiam fuga dicta nam autem odit error non quaerat rem itaque, provident ab sequi obcaecati aliquam possimus id eos quas voluptatem ullam ea, perspiciatis sapiente impedit iste dolore voluptates, nihil placeat libero possimus cumque nemo quod nulla adipisci ad pariatur. Ipsa ea quia similique quas fuga culpa nemo corporis nostrum voluptatem velit, rerum repellat doloribus qui veritatis quod dicta aliquam necessitatibus nihil. Harum repellendus saepe dolore laudantium voluptatem accusantium rem ad quibusdam animi, velit natus iusto hic provident, perspiciatis ipsa est atque hic?",
        "assigned_to": 10,
        "watchers": []
    },
    {
        "tags": [
            "ullam",
            "modi"
        ],
        "comment": "",
        "is_closed": false,
        "id": 10,
        "ref": 11,
        "owner": 10,
        "status": 7,
        "severity": 2,
        "priority": 1,
        "type": 1,
        "milestone": null,
        "project": 1,
        "created_date": "2013-12-20T09:54:00.212Z",
        "modified_date": "2013-12-20T09:54:00.259Z",
        "finished_date": null,
        "subject": "Support for bulk actions",
        "description": "Assumenda nobis excepturi ab nisi sint accusantium deserunt non eius, cumque iure ex quod nostrum consectetur fugit. Error eius excepturi, ullam doloremque excepturi voluptatem pariatur?",
        "assigned_to": 2,
        "watchers": []
    },
    {
        "tags": [
            "cumque",
            "repellat"
        ],
        "comment": "",
        "is_closed": false,
        "id": 11,
        "ref": 12,
        "owner": 8,
        "status": 1,
        "severity": 3,
        "priority": 2,
        "type": 1,
        "milestone": null,
        "project": 1,
        "created_date": "2013-12-20T09:54:00.272Z",
        "modified_date": "2013-12-20T09:54:00.272Z",
        "finished_date": null,
        "subject": "Migrate to Python 3 and milk a beautiful cow",
        "description": "Quos reprehenderit aliquid enim quasi illum neque mollitia expedita doloribus, eum porro corrupti libero quaerat iste delectus quos ea quam debitis? Enim quibusdam temporibus tempore commodi fugit reprehenderit, autem soluta sapiente dolorum iste magni praesentium neque, doloremque minima voluptatum sequi libero voluptate quisquam, ad possimus labore eos similique delectus at quis aliquam sint consequatur dignissimos.",
        "assigned_to": null,
        "watchers": []
    },
    {
        "tags": [
            "ullam",
            "veritatis"
        ],
        "comment": "",
        "is_closed": false,
        "id": 12,
        "ref": 13,
        "owner": 1,
        "status": 2,
        "severity": 3,
        "priority": 3,
        "type": 1,
        "milestone": null,
        "project": 1,
        "created_date": "2013-12-20T09:54:00.309Z",
        "modified_date": "2013-12-20T09:54:00.342Z",
        "finished_date": null,
        "subject": "Lighttpd x-sendfile support",
        "description": "Fugit voluptatum minima vitae quasi dignissimos deserunt? Tempora quos culpa dicta assumenda minus quasi esse perspiciatis ad ullam qui, quidem aliquid aspernatur dolore voluptatum eos possimus fugit asperiores repellendus ad, itaque ex natus doloremque quos assumenda provident a quisquam tempora?",
        "assigned_to": 7,
        "watchers": []
    },
    {
        "tags": [
            "voluptatibus",
            "explicabo"
        ],
        "comment": "",
        "is_closed": false,
        "id": 13,
        "ref": 14,
        "owner": 1,
        "status": 5,
        "severity": 1,
        "priority": 1,
        "type": 1,
        "milestone": null,
        "project": 1,
        "created_date": "2013-12-20T09:54:00.358Z",
        "modified_date": "2013-12-20T09:54:00.363Z",
        "finished_date": null,
        "subject": "Add setting to allow regular users to create folders at the root level.",
        "description": "Reprehenderit quis laborum ratione voluptatibus illum fugit molestias cumque, nihil voluptatem hic voluptates harum placeat est officia dolores itaque quas, laborum optio quis, voluptate atque delectus cum odio, culpa mollitia quod explicabo itaque nemo placeat sit repudiandae fuga. Reiciendis dolorum aspernatur? Cumque omnis provident quaerat ullam non, illum velit nihil reiciendis, accusantium ipsam unde dolore reiciendis nobis quam dolorem tempora culpa adipisci.",
        "assigned_to": 4,
        "watchers": []
    },
    {
        "tags": [
            "earum",
            "amet"
        ],
        "comment": "",
        "is_closed": false,
        "id": 14,
        "ref": 15,
        "owner": 3,
        "status": 5,
        "severity": 2,
        "priority": 3,
        "type": 1,
        "milestone": null,
        "project": 1,
        "created_date": "2013-12-20T09:54:00.376Z",
        "modified_date": "2013-12-20T09:54:00.511Z",
        "finished_date": null,
        "subject": "Support for bulk actions",
        "description": "Quam nisi omnis id consequuntur labore pariatur laboriosam fugiat quis quia reprehenderit, eius ipsum nam nesciunt impedit aspernatur, vitae porro facere quod numquam rem temporibus impedit modi? Aperiam quaerat dolorem provident reprehenderit quod, provident neque ipsa laudantium, illo eum nemo veritatis ut labore, ipsam distinctio harum similique voluptates beatae labore cupiditate, itaque suscipit maxime. Dolorum ab dolorem quasi harum?",
        "assigned_to": 5,
        "watchers": []
    },
    {
        "tags": [
            "magnam",
            "quaerat"
        ],
        "comment": "",
        "is_closed": false,
        "id": 15,
        "ref": 16,
        "owner": 4,
        "status": 5,
        "severity": 2,
        "priority": 3,
        "type": 1,
        "milestone": null,
        "project": 1,
        "created_date": "2013-12-20T09:54:00.525Z",
        "modified_date": "2013-12-20T09:54:00.528Z",
        "finished_date": null,
        "subject": "Lighttpd support",
        "description": "Amet magnam dolor quo accusantium voluptatem magni optio, nostrum asperiores eveniet dolorum assumenda illum ipsam, corrupti alias ducimus sit autem sapiente eos aperiam, nesciunt iusto nostrum iure eligendi culpa velit? Quia amet magnam corrupti totam dicta pariatur iure eos, nostrum eos fuga iusto, maiores nesciunt obcaecati nostrum enim doloribus nisi recusandae, unde eligendi cumque nesciunt suscipit ratione. Placeat accusamus sequi libero quisquam eos a numquam odit, rerum vero possimus veniam similique tenetur labore, ipsa commodi nemo obcaecati autem eum sit. Adipisci assumenda laudantium.",
        "assigned_to": 1,
        "watchers": []
    },
    {
        "tags": [
            "facilis",
            "quaerat",
            "consequatur",
            "cumque"
        ],
        "comment": "",
        "is_closed": false,
        "id": 16,
        "ref": 17,
        "owner": 10,
        "status": 5,
        "severity": 3,
        "priority": 2,
        "type": 1,
        "milestone": null,
        "project": 1,
        "created_date": "2013-12-20T09:54:00.543Z",
        "modified_date": "2013-12-20T09:54:00.589Z",
        "finished_date": null,
        "subject": "Support for bulk actions",
        "description": "Assumenda placeat animi, consequatur cupiditate autem commodi temporibus enim repellat ipsam atque libero voluptas, facilis nulla autem quia voluptatem quod minima dicta, esse sint eligendi impedit vel corporis nisi repellendus rem. Impedit architecto consequatur velit eius necessitatibus quod quas vel labore possimus, ullam sapiente magni autem, consequatur doloremque commodi asperiores dolore dicta quos quo voluptatem distinctio assumenda fugit, distinctio accusantium quo dolores? Consequuntur optio error ullam voluptas nam magni earum perferendis doloribus, facere quia perspiciatis placeat voluptates?",
        "assigned_to": 7,
        "watchers": []
    },
    {
        "tags": [
            "deserunt",
            "iure"
        ],
        "comment": "",
        "is_closed": false,
        "id": 17,
        "ref": 18,
        "owner": 7,
        "status": 2,
        "severity": 4,
        "priority": 3,
        "type": 1,
        "milestone": null,
        "project": 1,
        "created_date": "2013-12-20T09:54:00.602Z",
        "modified_date": "2013-12-20T09:54:00.670Z",
        "finished_date": null,
        "subject": "Add tests for bulk operations",
        "description": "Excepturi accusamus numquam a consequatur, provident qui nam iure dolorum voluptatum nulla natus cum fuga quidem, tempore provident quia ut illum eius corrupti ullam molestiae?",
        "assigned_to": 2,
        "watchers": []
    },
    {
        "tags": [
            "temporibus"
        ],
        "comment": "",
        "is_closed": true,
        "id": 18,
        "ref": 19,
        "owner": 10,
        "status": 6,
        "severity": 2,
        "priority": 3,
        "type": 1,
        "milestone": null,
        "project": 1,
        "created_date": "2013-12-20T09:54:00.684Z",
        "modified_date": "2013-12-20T09:54:00.753Z",
        "finished_date": "2013-12-20T09:54:00.681Z",
        "subject": "Fixing templates for Django 1.6.",
        "description": "Deserunt incidunt debitis numquam hic, accusantium magnam dolore assumenda temporibus velit laudantium labore repellendus autem, libero maxime eaque id repellendus possimus accusantium expedita corporis, odio obcaecati delectus quidem iure dolorum autem deleniti soluta debitis rerum, iure corporis quos cum ipsa? Illum inventore minima laudantium qui at obcaecati saepe, beatae exercitationem eos corporis dolorem soluta ad in harum quasi? Sapiente ipsam recusandae quidem vero laboriosam laudantium ratione corrupti at? Reiciendis aliquam aut sint unde temporibus iure quia, culpa laudantium sint natus alias vero, sapiente in ea nesciunt quod voluptatum.",
        "assigned_to": 9,
        "watchers": []
    },
    {
        "tags": [
            "expedita",
            "natus",
            "tenetur",
            "assumenda",
            "eos"
        ],
        "comment": "",
        "is_closed": false,
        "id": 19,
        "ref": 20,
        "owner": 8,
        "status": 5,
        "severity": 3,
        "priority": 3,
        "type": 1,
        "milestone": null,
        "project": 1,
        "created_date": "2013-12-20T09:54:00.766Z",
        "modified_date": "2013-12-20T09:54:00.770Z",
        "finished_date": null,
        "subject": "Fixing templates for Django 1.6.",
        "description": "Repellat voluptate eos dicta laudantium recusandae dignissimos quasi expedita impedit, sed ea nulla minus, nobis autem molestias velit ab laborum, beatae nostrum perferendis pariatur aliquam, provident distinctio commodi modi ipsam eos. Adipisci optio saepe corporis aperiam distinctio doloribus consequatur, cum alias aliquam voluptate repellendus natus officiis sed commodi dignissimos reprehenderit, officiis cum nostrum voluptas eligendi iusto doloribus illo dolor. Repudiandae dolores labore similique maiores assumenda, maiores sapiente ducimus rerum earum quo ab quis iusto, ullam tempore velit commodi molestias, quas magnam sed quia tempore sunt non quam dignissimos quaerat quo voluptate, iste illum reiciendis est quod itaque perspiciatis deserunt magni rerum? Quaerat delectus laborum, quos molestiae repellat cupiditate doloribus aliquam ea facere iste.",
        "assigned_to": 7,
        "watchers": []
    },
    {
        "tags": [
            "consectetur"
        ],
        "comment": "",
        "is_closed": false,
        "id": 20,
        "ref": 21,
        "owner": 9,
        "status": 7,
        "severity": 2,
        "priority": 2,
        "type": 1,
        "milestone": null,
        "project": 1,
        "created_date": "2013-12-20T09:54:00.783Z",
        "modified_date": "2013-12-20T09:54:00.835Z",
        "finished_date": null,
        "subject": "Lighttpd x-sendfile support",
        "description": "Eligendi quidem delectus aliquid dolorum placeat minus suscipit quisquam, quo illo repudiandae, autem pariatur modi sapiente totam fuga eum? Repudiandae explicabo animi nisi nesciunt enim odit architecto, reiciendis maiores alias at magni iusto commodi atque sint, consequatur enim ipsa optio officiis, quos deserunt eos fugiat nam numquam ullam necessitatibus cum distinctio incidunt, doloribus amet sapiente sunt fugiat magni ea praesentium. Ex voluptas magnam vitae, velit aliquam maxime repudiandae nam fugiat atque libero possimus vero doloribus. Suscipit vitae cumque ipsa.",
        "assigned_to": 10,
        "watchers": []
    }
]
"""
