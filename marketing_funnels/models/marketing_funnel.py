# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#

import json
import logging
import random
import re
from datetime import datetime
from sys import exc_info
from traceback import format_exception

from dateutil.relativedelta import relativedelta
from odoo import _, api, fields, models
from odoo.addons.http_routing.models.ir_http import slug
from odoo.exceptions import UserError, ValidationError
from odoo.tools import html2plaintext
from odoo.tools.safe_eval import safe_eval
from odoo.tools.translate import html_translate

_logger = logging.getLogger(__name__)

_intervalTypes = {
    'hours': lambda interval: relativedelta(hours=interval),
    'days': lambda interval: relativedelta(days=interval),
    'months': lambda interval: relativedelta(months=interval),
    'years': lambda interval: relativedelta(years=interval),
}


class FunnelType(models.Model):
    _name = 'funnel.type'
    _description = 'Funnel Type'

    name = fields.Char('Funnel Type', required=True, translate=True)
    description= fields.Text('Description')

class FunnelPageType(models.Model):
    _name = 'funnel.page.type'
    _description = 'Funnel Page Type'
    _order = 'sequence'

    name = fields.Char('Funnel Page Type', required=True, translate=True)
    sequence = fields.Integer('Sequence', help="Determine the display order", index=True)
    resource = fields.Selection([
        ('product','Product'),
        ('offer', 'Offer'),
        ('catalog', 'Catalog'), 
        ('random', 'Random'), 
        ('promotion', 'Promotion'),
        ('event','Event'),
        ('newsletter','Newsletter'),
        ('lead','Lead'),
        ('coupon_program','Coupon Program'),
        ('badge','Badge'),
        ('none','None')], required=True, default="none")
    funnel_types_ids = fields.Many2many('funnel.type', 'funnel_page_funnel_type_rel', 'page_id', 'funnel_type_id', string="Funnels Type", help='Visible in these type of funnels')

class FunnelPageStyle(models.Model):
    _name = 'funnel.page.style'
    _description = 'Funnel Page Style'

    name = fields.Char('Name', required=True, translate=True)
    theme_class = fields.Char('Class')


class Funnel(models.Model):
    _name = 'funnel.funnel'
    _description = 'Funnel'
    _inherit = ['mail.thread']
    _order = 'name'

    def _expand_buyer_journey(self, states, domain, order):
        return ['awareness','consideration','purchase','service', 'loyalty']  

    name = fields.Char('Funnel Name', required=True, translate=True)
    type_id = fields.Many2one('funnel.type', required=True)
    color = fields.Integer('Kanban Color Index')
    social_proof_interval = fields.Integer('Social Proof Interval', default= 5, help='Maximum tracking time in hours')
    parent_funnel_id = fields.Many2one('funnel.funnel', 'Parent Funnel')
    child_funnel_id = fields.Many2one('funnel.funnel', 'Child Funnel')
    buyer_journey_stage = fields.Selection([('awareness','Awareness'),('consideration','Consideration'),('purchase','Purchase'),('service','Service'),('loyalty','Loyalty')], string="Buyer's Journey Stage", default='awareness', required=True, copy=False, track_visibility='onchange', group_expand='_expand_buyer_journey')
    pages_ids = fields.One2many('funnel.page', inverse_name="funnel_id")
    website_id = fields.Many2one('website', required=True)
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)  

class FunnelPage(models.Model):
    _name = 'funnel.page'
    _description = 'Funnel Page'   
    _inherit = ['mail.thread', 'website.seo.metadata', 'website.published.multi.mixin']
    _order = 'name'

    def _default_content(self):
        return '''
            <p class="o_default_snippet_text">''' + _("Start writing here...") + '''</p>
        '''

    def _compute_website_url(self):
        super(FunnelPage, self)._compute_website_url()
        for funnel_page in self:
            if funnel_page.id:
                funnel_page.website_url = "/touchpoint/%s/page/%s" % (slug(funnel_page.funnel_id), slug(funnel_page))

    def _get_funnels_types(self):
        if 'params' in self.env.context.keys():
            if 'id' in self.env.context['params'].keys():
                funnel_id = self.env.context['params']['id']
                funnel_type = self.env['funnel.funnel'].browse(funnel_id).type_id
                res = []
                for page_type in  self.env['funnel.page.type'].search([]):
                    if funnel_type in page_type.funnel_ids:
                        res.append( page_type.id)
        return [('funnel_ids', 'in',res)]



    name = fields.Char('Page Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', help="Determine the display order", index=True)
    funnel_id = fields.Many2one('funnel.funnel', 'Funnel', required=True, ondelete='cascade')
    type_id = fields.Many2one('funnel.page.type', required=True)
    active = fields.Boolean('Active', default=True)
    content_top = fields.Html('Top Content', default=_default_content, translate=html_translate, sanitize=False)
    content_bottom = fields.Html('Bottom Content', default=_default_content, translate=html_translate, sanitize=False)
    product_id = fields.Many2one(
        'product.template', string='Product', domain=[('sale_ok', '=', True)],
        change_default=True, check_company=True) 
    products_ids = fields.Many2many('product.template', 'funnel_page_product_rel', 'page_id', 'page_product_id', domain=[('sale_ok', '=', True)], string='Products')
    event_id = fields.Many2one('event.event')
    badge_id = fields.Many2one('gamification.badge')
    coupon_program_id = fields.Many2one('coupon.program')
    salesteam_id = fields.Many2one('crm.team',string='Sales Team')
    salesperson_id = fields.Many2one('res.users', string='Salesperson')
    lead_phone = fields.Selection([('not_necessary','Not necessary'),('requested','Requested'),('required','Required')], default='requested', required=True)
    lead_company = fields.Selection([('not_necessary','Not necessary'),('requested','Requested'),('required','Required')], default='requested', required=True)
    lead_subject = fields.Selection([('required','Required'),('hidden','Hidden')], default='required', required=True)
    lead_name = fields.Char()
    lead_question = fields.Selection([('not_necessary','Not necessary'),('requested','Requested'),('required','Required')], default='required', required=True)
    call_to_action = fields.Selection([
        ('suscribe','Subscribe'), 
        ('apply','Apply'),
        ('reserve','Reserve'),
        ('download','Download'),
        ('get_offer','Get Offer'),
        ('quote','Quote'),
        ('sign_up','Sign Up'),
        ('more_info','More Information')
        ], string='Call to Action', default='more_info', required=True)
    button_position = fields.Selection([('left','Left'),('center','Center'),('right','Right'),('input_aligned','Input Aligned')], default='input_aligned', required=True)
    success_page = fields.Many2one('funnel.page')
    has_zoom = fields.Boolean(default=False)
    has_buy_now = fields.Boolean(default=True)
    catalogue_mode = fields.Selection([('p_cards', 'Products Cards'), ('p_carousel','Carousel Products'), ('s_cards','Card Services'),('s_carousel','Carousel Services')],
                                    default='p_cards')
    random_product = fields.Boolean(default=False)
    style_id = fields.Many2one('funnel.page.style')
    mailing_list_id = fields.Many2one('mailing.list', string='')
    resource = fields.Char(compute='_get_resource', store=True)
    social_proof_notification = fields.Boolean('Social Proof Notifications', default=False, help='')
    last_date = fields.Datetime('Last View')
    visits = fields.Integer('No of Views', copy=False, readonly=True)
    is_published = fields.Boolean(default=False)
    website_id = fields.Many2one(related='funnel_id.website_id', readonly=True)
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company) 

    @api.depends('type_id')
    def _get_resource(self):
        for record in self:
            record.resource = self.type_id.resource

    
    def process_activities(self, page_id, visitor_id):
        return True


