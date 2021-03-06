# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#

from odoo import api, fields, models, tools, _

class MarketingBasicNeeds(models.Model):

    _name = "marketing_strategy.consumer_trend.basic_need"
    _description = "Basic Needs"

    name = fields.Char('Name', required=True, translate=True, readonly=True)
    color = fields.Integer('Color Index', readonly=True)

class MarketingInnovationType(models.Model):

    _name = "marketing_strategy.consumer_trend.innovation_type"
    _description = "Innovation Type"

    name = fields.Char('Name', required=True, translate=True, readonly=True)
    color = fields.Integer('Color Index', readonly=True)

class MarketingQuestionS(models.Model):

    _name = "marketing_strategy.consumer_trend.question_s"
    _description = "SCAMPER Question S"

    name = fields.Char('Question', required=True, translate=True)
    sequence = fields.Integer('Sequence')
    consumer_trend_id = fields.Many2one('marketing_strategy.consumer_trend', required=True)

class MarketingQuestionC(models.Model):

    _name = "marketing_strategy.consumer_trend.question_c"
    _description = "SCAMPER Question C"
    _inherit = "marketing_strategy.consumer_trend.question_s"

class MarketingQuestionA(models.Model):

    _name = "marketing_strategy.consumer_trend.question_a"
    _description = "SCAMPER Question A"
    _inherit = "marketing_strategy.consumer_trend.question_s"

class MarketingQuestionM(models.Model):

    _name = "marketing_strategy.consumer_trend.question_m"
    _description = "SCAMPER Question M"
    _inherit = "marketing_strategy.consumer_trend.question_s"

class MarketingQuestionP(models.Model):

    _name = "marketing_strategy.consumer_trend.question_p"
    _description = "SCAMPER Question P"
    _inherit = "marketing_strategy.consumer_trend.question_s"


class MarketingQuestionE(models.Model):

    _name = "marketing_strategy.consumer_trend.question_e"
    _description = "SCAMPER Question E"
    _inherit = "marketing_strategy.consumer_trend.question_s"

class MarketingQuestionR(models.Model):

    _name = "marketing_strategy.consumer_trend.question_r"
    _description = "SCAMPER Question R"
    _inherit = "marketing_strategy.consumer_trend.question_s"
   
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
    needs_ids = fields.Many2many('marketing_strategy.need')
    tribes_ids = fields.Many2many('marketing_strategy.tribe', 'marketing_strategy_consumer_trend_tribe_rel', 'consumer_trend_id', 'tribe_id')
    what_change = fields.Text()
    mode = fields.Selection([('incremental','Incremental'),('architectural','Architectural'),('disruptive','Disruptive'),('radical','Radical')])
    innovation_type = fields.Many2many('marketing_strategy.consumer_trend.innovation_type','marketing_strategy_custumer_trend_innovation_type_rel','custumer_trend_id', 'type_id')
    questions_s_ids = fields.One2many('marketing_strategy.consumer_trend.question_s', 'consumer_trend_id')
    questions_c_ids = fields.One2many('marketing_strategy.consumer_trend.question_c', 'consumer_trend_id')
    questions_a_ids = fields.One2many('marketing_strategy.consumer_trend.question_a', 'consumer_trend_id')
    questions_m_ids = fields.One2many('marketing_strategy.consumer_trend.question_m', 'consumer_trend_id')
    questions_p_ids = fields.One2many('marketing_strategy.consumer_trend.question_p', 'consumer_trend_id')
    questions_e_ids = fields.One2many('marketing_strategy.consumer_trend.question_e', 'consumer_trend_id')
    questions_r_ids = fields.One2many('marketing_strategy.consumer_trend.question_r', 'consumer_trend_id')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)