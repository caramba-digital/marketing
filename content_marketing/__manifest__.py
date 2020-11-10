# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#
{
    'name': "Content Marketing",

    'summary': "Content management on the buyer's journey",

    'author': "Antonio Fregoso",
    'website': "http://www.antoniofregoso.com",
    'category': "Marketing/Content",
    'version': '0.0.2',
    'depends': ['marketing_strategy', 'website_blog'],
    'license': 'AGPL-3',
    'data': [
        'security/content_marketing_security.xml',
        'security/ir.model.access.csv',
        'views/views_content_marketing.xml',
        'views/website_blog_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],   
    
    'installable': True,
    'application': True,
    'auto_install': False
}
