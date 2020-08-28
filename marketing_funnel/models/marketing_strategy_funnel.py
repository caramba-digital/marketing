# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#

from datetime import datetime
import random
import json

from odoo import api, models, fields, _
from odoo.addons.http_routing.models.ir_http import slug
from odoo.tools.translate import html_translate
from odoo.tools import html2plaintext

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

class FunnelPageType(models.Model):
    _name = 'funnel.page.type'
    _description = 'Funnel Page Type'

    name = fields.Char('Funnel Type', required=True, translate=True)


class Funnel(models.Model):
    _name = 'funnel.funnel'
    _description = 'Funnel'
    _inherit = ['mail.thread', 'website.multi.mixin']
    _order = 'name'

    def _expand_buyer_journey(self, states, domain, order):
        return ['awareness','consideration','purchase','service', 'loyalty']  

    name = fields.Char('Funnel Name', required=True, translate=True)
    type_id = fields.Many2one('funnel.type', required=True)
    brand_id = fields.Many2one('marketing_strategy.brand', domain = [('relation','=', 'main')], string='Brand', required=True)
    color = fields.Integer('Kanban Color Index')
    parent_funnel_id = fields.Many2one('funnel.funnel', 'Parent Funnel')
    child_funnel_id = fields.Many2one('funnel.funnel', 'Child Funnel')
    buyer_journey_stage = fields.Selection([('awareness','Awareness'),('consideration','Consideration'),('purchase','Purchase'),('service','Service'),('loyalty','Loyalty')], string="Buyer's Journey Stage", default='awareness', required=True, copy=False, track_visibility='onchange', group_expand='_expand_buyer_journey')
    pages_ids = fields.One2many('funnel.page', inverse_name="funnel_id")
  
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
            funnel_page.website_url = "/touchpoint/%s/page/%s" % (slug(funnel_page.funnel_id), slug(funnel_page))


    name = fields.Char('Page Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', help="Determine the display order", index=True)
    type_id = fields.Many2one('funnel.page.type', required=True)
    active = fields.Boolean('Active', default=True)
    content = fields.Html('Content', default=_default_content, translate=html_translate, sanitize=False)
    funnel_id = fields.Many2one('funnel.funnel', 'Funnel', required=True, ondelete='cascade')
    visits = fields.Integer('No of Views', copy=False)
    website_id = fields.Many2one(related='funnel_id.website_id', readonly=True)
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)  

    

class FunnelActivity(models.Model):
    _name = 'funnel.activity'
    _description = 'Funnel Activity"' 

    name = fields.Char('Funnel Phase', required=True, translate=True)
    action_type = fields.Selection([('email','Email'), ('report','Report'), ('action', 'Custom Action')], default='email',
    help="The type of action to execute when an item enters this activity, such as:\n"
             "- Email: send an email using a predefined email template \n"
             "- Report: print an existing Report defined on the resource item and save it into a specific directory \n"
             "- Custom Action: execute a predefined action, e.g. to modify the fields of the resource record")
    email_template_id = fields.Many2one('mail.template', 'Email Template', help='The email to send when this activity is activated')
    report_id = fields.Many2one('ir.actions.report.xml', 'Report', help='The report to generate when this activity is activated')
    server_action_id = fields.Many2one('ir.actions.server', string='Action', help='The action to perform when this activity is activated')
    
   