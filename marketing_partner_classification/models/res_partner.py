# -*- coding: utf-8 -*-
# LICENSE GNU GENERAL PUBLIC LICENSE Version 3 

from odoo import fields,api, models, _


class PartnerPlatform(models.Model):
    _name = 'res.partner.platform'
    _description = 'Digital Platform'
    _order = 'name'

    name = fields.Char(string='Platform')

class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    #Digitization
    crm = fields.Boolean('CRM')
    sales = fields.Boolean('Sales')
    ecommerce = fields.Boolean('eCommerce')
    purchase = fields.Boolean('Purchase')
    inventory = fields.Boolean('Inventory')
    mrp = fields.Boolean('MRP')
    online_presence = fields.Boolean('Online Presence')
    hr = fields.Boolean('HR')
    fleet = fields.Boolean('Fleet')
    marketing = fields.Boolean('Marketing')
    finances = fields.Boolean('Finances')
    war_room = fields.Boolean('War Room')
    #Consulting

    marketing_campaign = fields.Boolean('Marketing Campaign')
    business_model = fields.Boolean('Business Model')
    innovation = fields.Boolean('Innovation')
    trainning = fields.Boolean('Training')

    #Classification
    stores = fields.Integer('Stores')
    sales_floor = fields.Integer('Sales Floor')
    employees = fields.Integer('Employees', help="Number of employees")
    turnover = fields.Monetary('Turnover', currency_field='company_currency')
    assets = fields.Monetary('Assets', currency_field='company_currency')
    digitization_level = fields.Selection([('beginner','Beginner'),('medium','Medium'),('advanced','Advanced'),('expert','Expert')], string='Digitization Level', default='beginner')
    platform_id = fields.Many2one('res.partner.platform', string='Platform')
    company_currency = fields.Many2one('res.currency', related='company_id.currency_id')


