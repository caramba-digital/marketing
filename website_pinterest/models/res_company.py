# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Company(models.Model):
    _inherit = "res.company"

    social_pinterest = fields.Char('Pinterest Account')