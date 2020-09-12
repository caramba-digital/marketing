# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#

from odoo import fields, models, api


class WebsiteVisitor(models.Model):
    _inherit = 'website.visitor'

    funnel_ids  = fields.Many2one('funnel.funnel', string='Funnels', help="Completed Funnels", groups='marketing_strategy.group_strategy_user')
    funnel_pages_ids = fields.Many2one('funnel.page', string='Funnel Pages', groups='marketing_strategy.group_strategy_user')
    funnel_count = fields.Integer('# Funnels', compute="_compute_funnel_count", groups='marketing_strategy.group_strategy_user')

    @api.depends('funnel_ids')
    def _compute_funnel_count(self):
        for visitor in self:
            visitor.funnel_count = len(visitor.funnel_ids)
     
    