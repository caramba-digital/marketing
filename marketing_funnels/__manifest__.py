# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#

{
    'name': "Marketing Funnels",

    'summary': "Second-Generation Sales Funnels",

    'author': "Antonio Fregoso",
    'website': "https://antoniofregoso.com",
 

    'category': 'Marketing/Funnels',
    'version': '0.0.1',

    'depends': ['crm', 'website_sale_coupon', 'website_event', 'gamification', 'mass_mailing', 
                        'website_services','website_animated','website_swiper'],


    'data': [
        'security/marketing_funnels_security.xml',
        'security/ir.model.access.csv',
        'views/marketing_funnels_templates.xml',
        'views/marketing_funnels_views.xml',
        'views/marketing_funnels_settings_views.xml',
        'views/mail_template_views.xml',
        'views/assets.xml',
        'data/marketing_funnels_data.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ], 
    
    'installable': True,
    'application': True,
    'auto_install': False
}
