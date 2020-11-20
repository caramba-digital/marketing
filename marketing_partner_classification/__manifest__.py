# -*- coding: utf-8 -*-
{
    'name': "Partner Classification",

    'summary': "Partner Classification for digitization",

    'author': "Antonio Fregoso",
    'website': "http://antoniofregoso.com",
    'category': 'Marketing/Strategy',
    'depends': ['marketing_strategy'],
    'license': 'AGPL-3',
    'data': [
         'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'data/marketing_partner_classification_data.xml'
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
