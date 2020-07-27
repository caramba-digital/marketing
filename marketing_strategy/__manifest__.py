# -*- coding: utf-8 -*-
{
    'name': "Marketing Strategy",

    'summary': "Marketing Strategy Framework",


    'author': "Antonio Fregoso",
    'website': "https://antoniofregoso.com",
    'category': 'Marketing/Strategy',
    'version': '13.0.0.0.0',
    'depends': ['mail','sale'],
    'license': 'AGPL-3',
    'data': [
        'security/marketing_strategy_security.xml',
        'views/utm_views.xml',
        'views/marketing_strategy_settings_views.xml',
        
    ],
    'demo': [
        'demo/demo.xml',
    ],    
    
    'installable': True,
    'application': True,
    'auto_install': False
}
