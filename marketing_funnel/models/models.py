# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class marketing_funnel(models.Model):
#     _name = 'marketing_funnel.marketing_funnel'
#     _description = 'marketing_funnel.marketing_funnel'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
