# -*- coding: utf-8 -*-
# from odoo import http


# class WebsitePinterest(http.Controller):
#     @http.route('/website_pinterest/website_pinterest/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/website_pinterest/website_pinterest/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('website_pinterest.listing', {
#             'root': '/website_pinterest/website_pinterest',
#             'objects': http.request.env['website_pinterest.website_pinterest'].search([]),
#         })

#     @http.route('/website_pinterest/website_pinterest/objects/<model("website_pinterest.website_pinterest"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('website_pinterest.object', {
#             'object': obj
#         })
