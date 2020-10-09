# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#
from odoo import api, fields, models

class CustomerChannel(models.Model):

    _name = "marketing_strategy.channel"
    _description = "Channel"

    name = fields.Char('Name', required=True, translate=True)
    color = fields.Integer('Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Channel already exists !"),
    ]

class KeyActivities(models.Model):

    _name = "marketing_strategy.key_activity"
    _description = "Key Activity"

    name = fields.Char('Name', required=True, translate=True)
    color = fields.Integer('Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Ativity already exists !"),
    ]
    
class KeyResourcePhysical(models.Model):

    _name = "marketing_strategy.key_resource_physical"

    _description = "Key Resource"

    name = fields.Char('Tag Name', required=True, translate=True)
    color = fields.Integer('Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Resource name already exists !"),
    ]
    
class KeyResourceFinancial(models.Model):

    _name = "marketing_strategy.key_resource_financial"
    _description = "Key Financial Resource"

    name = fields.Char('Tag Name', required=True, translate=True)
    color = fields.Integer('Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Resource name already exists !"),
    ]


class KeyResourceIntellectual(models.Model):

    _name = "marketing_strategy.key_resource_intellectual"
    _description = "Key Intellectual Resource"

    name = fields.Char('Tag Name', required=True, translate=True)
    color = fields.Integer('Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Resource name already exists !"),
    ]


class KeyResource(models.Model):

    _name = "marketing_strategy.key_resource"
    _description = "Key Resource"

    name = fields.Char('Tag Name', required=True, translate=True)
    color = fields.Integer('Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Resource name already exists !"),
    ]

class BusinessModel(models.Model):
    _name = "marketing_strategy.business_model"
    _description = "Business Model Canvas"
    _inherit = ['mail.thread', 'mail.activity.mixin','image.mixin']

    def _expand_states(self, states, domain, order):
        return ['draft', 'active', 'done', 'cancel']

    name =  fields.Char('Name', required=True)
    description = fields.Html('Description')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('done', 'Completed'),
        ('cancel', 'Cancelled'),
        ],
        string='Status', default='draft', required=True, copy=False, track_visibility='onchange', group_expand='_expand_states')
    active = fields.Boolean(default=True)
    user_id = fields.Many2one('res.users', string='Responsible', default=lambda self: self.env.user, track_visibility="onchange")
    color = fields.Integer('Kanban Color Index')
    date_begin = fields.Date()
    date_end = fields.Date()
    buyers_persona_ids = fields.Many2many('marketing_strategy.buyer_persona', 'marketing_strategy_business_model_buyer_persona_rel', 'business_plan_id', 'buyer_persona_id')
    value_proposition_ids = fields.Many2many('marketing_strategy.value_proposition', 'marketing_strategy_business_plan_value_proposition_rel', 'business_plan_id', 'value_proposition_id')
    story_brand_ids = fields.Many2many('marketing_strategy.story_brand', 'marketing_strategy_business_plan_story_brand_rel', 'busoness_plan_id', 'story_brand_id')
    channels_ids = fields.Many2many('marketing_strategy.channel', 'marketing_strategy_business_plan_channel_rel', 'model_id', 'channel_id')
    key_partners_ids = fields.Many2many('res.partner')
    key_activities_ids = fields.Many2many('marketing_strategy.key_activity','marketing_strategy_business_model__activity_rel','business_model_id','activity_id')
    key_resource_physical_ids = fields.Many2many('marketing_strategy.key_resource_physical', 'marketing_strategy_business_model_resource_physical_rel', 'business_model_id', 'resource_id')
    key_human_resources_ids = fields.Many2many('res.partner', 'marketing_strategy_human_resource_rel')
    key_resource_financial_ids = fields.Many2many('marketing_strategy.key_resource_financial', 'marketing_strategy_business_model_resource_financial_rel', 'business_model_id', 'resource_id')
    key_resource_intellectual_ids = fields.Many2many('marketing_strategy.key_resource_intellectual', 'marketing_strategy_business_model_resource_intellectual_rel', 'business_model_id', 'resource_id')
    key_resource_ids = fields.Many2many('marketing_strategy.key_resource', 'marketing_strategy_business_plan_resource_rel', 'business_model_id', 'resource_id')
    cost_structure_ids = fields.Many2many('account.account', 'marketing_strategy_business_plan_cost_rel', 'business_plan_id', 'account_id',string="Cost Structure")
    revenue_streams_ids = fields.Many2many('account.account', 'marketing_strategy_business_plan_revenue_rel', 'business_plan_id', 'account_id',string="Revenue Streams")
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)
    
