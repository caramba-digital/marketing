# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#

{
    'name': "Marketing Business Model",

    'summary': "Live Business Model Canvas",

    'author': "Antonio Fregoso",
    'website': "https://www.antoniofregoso.com",
    'category': 'Marketing/Strategy',
    'version': '0.0.0',
    'license': 'AGPL-3',
    'depends': ['marketing_strategy'],
    'data': [
        'security/ir.model.access.csv',
        'security/marketing_strategy_security.xml',
        'views/marketing_strategy_views.xml',
        'views/marketing_strategy_story_brand_views.xml',
        'views/marketing_strategy_settings_views.xml',
        'data/marketing_business_model_data.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
