# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': "Project Scrum",

    'summary': "Use Scrum Method to manage your project",


    'author': "My Company",
    'website': "https://antoniofregoso.com",

    'category': 'Operations/Project',
    'version': '13.0.0.0',
    'depends': ['project','project_task_code', 'project_stage_state'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'installable': True,
    'license': 'AGPL-3',
    'application': True,
}
