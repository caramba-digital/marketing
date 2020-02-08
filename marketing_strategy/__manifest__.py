# -*- coding: utf-8 -*-
{
    'name': "Marketing Strategy",

    'summary': "Marketing Strategy Framework",


    'author': "Antonio Fregoso",
    'website': "https://antoniofregoso.com",
    'category': 'Marketing/Strategy',
    'version': '13.0.0.0.0',
    'depends': ['base','mail','project','crm','sale'],
    'license': 'AGPL-3',
    'data': [
        'security/marketing_strategy_security.xml',
        'security/ir.model.access.csv',
        'views/marketing_strategy_views.xml',
        'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
