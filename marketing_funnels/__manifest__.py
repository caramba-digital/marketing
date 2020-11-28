# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#

{
    'name': "Marketing Funnels",

    'summary': "Sales Funnels",

    'author': "Antonio Fregoso",
    'website': "https://antoniofregoso.com",
 

    'category': 'Marketing/Strategy',
    'version': '0.0.1',

    'depends': ['marketing_strategy', 'website_event', 'hr_gamification', 'mass_mailing'],


    'data': [
        'security/ir.model.access.csv',
        'views/marketing_strategy_funnel_templates.xml',
        'views/marketing_strategy_funnel_views.xml',
        'views/marketing_strategy_settings_views.xml',
        'views/mail_template_views.xml',
        'views/website_visitor_views.xml',
        'data/marketing_strategy_funnel_data.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
