# -*- coding: utf-8 -*-
# from odoo import http


# class MarketingStrategyGapAssessment(http.Controller):
#     @http.route('/marketing_strategy_gap_assessment/marketing_strategy_gap_assessment/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/marketing_strategy_gap_assessment/marketing_strategy_gap_assessment/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('marketing_strategy_gap_assessment.listing', {
#             'root': '/marketing_strategy_gap_assessment/marketing_strategy_gap_assessment',
#             'objects': http.request.env['marketing_strategy_gap_assessment.marketing_strategy_gap_assessment'].search([]),
#         })

#     @http.route('/marketing_strategy_gap_assessment/marketing_strategy_gap_assessment/objects/<model("marketing_strategy_gap_assessment.marketing_strategy_gap_assessment"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('marketing_strategy_gap_assessment.object', {
#             'object': obj
#         })
