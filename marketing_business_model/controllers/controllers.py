# -*- coding: utf-8 -*-
# from odoo import http


# class MarketingBusinessModel(http.Controller):
#     @http.route('/marketing_business_model/marketing_business_model/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/marketing_business_model/marketing_business_model/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('marketing_business_model.listing', {
#             'root': '/marketing_business_model/marketing_business_model',
#             'objects': http.request.env['marketing_business_model.marketing_business_model'].search([]),
#         })

#     @http.route('/marketing_business_model/marketing_business_model/objects/<model("marketing_business_model.marketing_business_model"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('marketing_business_model.object', {
#             'object': obj
#         })
