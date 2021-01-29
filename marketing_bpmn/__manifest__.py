# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#
{
    'name': "Marketing BPMN 2.0",

    'summary': "Marketing Business Process Model and Notation 2.0",

    'author': "Antonio Fregoso",
    'website': "http://www.antoniofregoso.com",

    'category': 'Marketing/bpmn',
    'version': '0.0.1',

    'depends': ['website'],

    'data': [
        'security/marketing_bpmn_security.xml',
        'security/ir.model.access.csv',
        'views/marketing_bpmn_views.xml',
        'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False
}

