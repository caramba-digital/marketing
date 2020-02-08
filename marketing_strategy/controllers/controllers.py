# -*- coding: utf-8 -*-
# from odoo import http


# class MarketingConsumerTrendCanvas(http.Controller):
#     @http.route('/marketing_strategy/marketing_strategy/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/marketing_strategy/marketing_strategy/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('marketing_strategy.listing', {
#             'root': '/marketing_strategy/marketing_strategy',
#             'objects': http.request.env['marketing_strategy.marketing_strategy'].search([]),
#         })

#     @http.route('/marketing_strategy/marketing_strategy/objects/<model("marketing_strategy.marketing_strategy"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('marketing_strategy.object', {
#             'object': obj
#         })
