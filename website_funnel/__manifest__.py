# -*- coding: utf-8 -*-
# LICENSE GNU GENERAL PUBLIC LICENSE Version 3

{
    'name': "Website Funnel",

    'summary': "Implement sales funnels",
      

    'author': "Antonio Fregoso",
    'website': "http://antoniofregoso.com",

   'category': 'Website/Marketing',
    'version': '0.0.0-alpha.1',

    'depends': ['website_swiper'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/website_funnel_views.xml',
        'views/website_funnel_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
