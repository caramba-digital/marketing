# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#

from odoo import api, fields, models


class Partner(models.Model):
    _inherit = 'res.partner'
    
    touchpoint_hub = fields.Boolean(string='Is a Touchpoints Hub', default=False,
                               help="Check this box if this locationt is a touchpoint.")
    brand_advocacy = fields.Selection([('does_not_apply','Does not apply'), ('employee_advocate','Employee Advocate'), ('customer_advocate','Customer Advocate'), ('ambassador','Ambassador'), ('influencer','Influencer')], default='does_not_apply')
    
    
