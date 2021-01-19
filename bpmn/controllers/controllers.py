# -*- coding: utf-8 -*-
# from odoo import http


# class Bpmn(http.Controller):
#     @http.route('/bpmn/bpmn/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bpmn/bpmn/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bpmn.listing', {
#             'root': '/bpmn/bpmn',
#             'objects': http.request.env['bpmn.bpmn'].search([]),
#         })

#     @http.route('/bpmn/bpmn/objects/<model("bpmn.bpmn"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bpmn.object', {
#             'object': obj
#         })
