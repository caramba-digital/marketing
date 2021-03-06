# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#

{
    'name': "Marketing Strategy Consumer Trend",

    'summary': "Implement the consumer trends canvas",

    'author': "Antonio Fregoso",
    'website': "https://antoniofregoso..com",

    'category': 'Marketing/Strategy',
    'version': '13.0.0.0.0',

    'depends': ['marketing_strategy'],

    'license': 'AGPL-3',

    'data': [
        'security/ir.model.access.csv',
        'views/marketing_strategy_views.xml',
        'data/marketing_strategy_data.xml',
    ],

    'demo': [
        'demo/demo.xml',
    ],
}
