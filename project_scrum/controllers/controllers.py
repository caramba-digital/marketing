# -*- coding: utf-8 -*-
# from odoo import http


# class ProjectScrum(http.Controller):
#     @http.route('/project_scrum/project_scrum/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/project_scrum/project_scrum/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('project_scrum.listing', {
#             'root': '/project_scrum/project_scrum',
#             'objects': http.request.env['project_scrum.project_scrum'].search([]),
#         })

#     @http.route('/project_scrum/project_scrum/objects/<model("project_scrum.project_scrum"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('project_scrum.object', {
#             'object': obj
#         })
