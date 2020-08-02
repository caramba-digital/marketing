# -*- coding: utf-8 -*-
# from odoo import http


# class MarketingFunnel(http.Controller):
#     @http.route('/marketing_funnel/marketing_funnel/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/marketing_funnel/marketing_funnel/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('marketing_funnel.listing', {
#             'root': '/marketing_funnel/marketing_funnel',
#             'objects': http.request.env['marketing_funnel.marketing_funnel'].search([]),
#         })

#     @http.route('/marketing_funnel/marketing_funnel/objects/<model("marketing_funnel.marketing_funnel"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('marketing_funnel.object', {
#             'object': obj
#         })
