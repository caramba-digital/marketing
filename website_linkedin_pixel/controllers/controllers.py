# -*- coding: utf-8 -*-
# from odoo import http


# class WebsiteLinkedinPixel(http.Controller):
#     @http.route('/website_linkedin_pixel/website_linkedin_pixel/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/website_linkedin_pixel/website_linkedin_pixel/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('website_linkedin_pixel.listing', {
#             'root': '/website_linkedin_pixel/website_linkedin_pixel',
#             'objects': http.request.env['website_linkedin_pixel.website_linkedin_pixel'].search([]),
#         })

#     @http.route('/website_linkedin_pixel/website_linkedin_pixel/objects/<model("website_linkedin_pixel.website_linkedin_pixel"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('website_linkedin_pixel.object', {
#             'object': obj
#         })
