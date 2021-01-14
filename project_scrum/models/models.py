# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class project_scrum(models.Model):
#     _name = 'project_scrum.project_scrum'
#     _description = 'project_scrum.project_scrum'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
