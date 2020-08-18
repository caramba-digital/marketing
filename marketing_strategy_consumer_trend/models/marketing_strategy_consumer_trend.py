# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#

from odoo import api, fields, models, tools, _

class MarketingInnovationType(models.Model):

    _name = "marketing_strategy.consumer_trend.innovation_type"
    _description = "Needs"

    name = fields.Char('Name', required=True, translate=True, readonly=True)
    color = fields.Integer('Color Index')

class MarketingStrategyConsumerTrend(models.Model):
    _name = "marketing_strategy.consumer_trend"
    _description = "Consumer Trend"
    _inherit = ['mail.thread', 'mail.activity.mixin','image.mixin']

    def _expand_states(self, states, domain, order):
        return ['draft', 'analyzing', 'done', 'cancel']
    

    name = fields.Char('Name', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('analyzing', 'Analyzing'),
        ('done', 'Completed'),
        ('cancel', 'Cancelled'),
        ],
        string='Status', default='draft', required=True, copy=False, track_visibility='onchange', group_expand='_expand_states')
    color = fields.Integer('Kanban Color Index')
    start = fields.Datetime()
    end = fields.Datetime()
    trend = fields.Text()
    innovation = fields.Text()
    mode = fields.Selection([('incremental','Incremental'),('architectural','Architectural'),('disruptive','Disruptive'),('radical','Radical')])
    innovation_type = fields.Many2many('marketing_strategy.consumer_trend.innovation_type','marketing_strategy_custumer_trend_innovation_type_rel','custumer_trend_id', 'type_id')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)