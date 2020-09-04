# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#

{
    'name': "marketing_funnel",

    'summary': "Sales Funnels",


    'author': "antonio fregoso",
    'website': "https://antoniofregoso.com",
    
    'category': 'Marketing/Strategy',
    'version': '13.0.0.0.0',
    'depends': ['marketing_strategy', 'website'],
    'license': 'AGPL-3',

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/marketing_strategy_funnel_templates.xml',
        'views/marketing_strategy_funnel_views.xml',
        'views/marketing_strategy_views.xml',
        'data/marketing_strategy_funnel_data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
