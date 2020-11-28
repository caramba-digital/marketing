# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#

from odoo import api, fields, models

class Touchpoint(models.Model):
    _name = "marketing_strategy.touchpoint"
    _inherit  = "marketing_strategy.touchpoint"

    funnel_id = fields.Many2one('funnel.funnel', 'Funnel')