# -*- coding: utf-8 -*-
# from odoo import http


# class MarketingConsumerTrendCanvas(http.Controller):
#     @http.route('/marketing_consumer_trend_canvas/marketing_consumer_trend_canvas/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/marketing_consumer_trend_canvas/marketing_consumer_trend_canvas/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('marketing_consumer_trend_canvas.listing', {
#             'root': '/marketing_consumer_trend_canvas/marketing_consumer_trend_canvas',
#             'objects': http.request.env['marketing_consumer_trend_canvas.marketing_consumer_trend_canvas'].search([]),
#         })

#     @http.route('/marketing_consumer_trend_canvas/marketing_consumer_trend_canvas/objects/<model("marketing_consumer_trend_canvas.marketing_consumer_trend_canvas"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('marketing_consumer_trend_canvas.object', {
#             'object': obj
#         })
