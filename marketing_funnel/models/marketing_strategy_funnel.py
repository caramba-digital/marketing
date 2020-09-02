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
    _inherit = ['mail.thread']
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
    website_id = fields.Many2one('website')
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
    object_id = fields.Many2one('ir.model',string='Resource')
    content = fields.Html('Content', default=_default_content, translate=html_translate, sanitize=False)
    funnel_id = fields.Many2one('funnel.funnel', 'Funnel', required=True, ondelete='cascade')
    activity_ids = fields.One2many('funnel.activity', 'page_id', 'Activities')
    visits = fields.Integer('No of Views', copy=False)
    is_published = fields.Boolean(default=False)
    website_id = fields.Many2one(related='funnel_id.website_id', readonly=True)
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)  



class FunnelActivity(models.Model):
    _name = 'funnel.activity'
    _description = 'Funnel Activity"' 

    name = fields.Char('Name', required=True, translate=True)
    object_id = fields.Many2one('ir.model', string='Object', readonly=True)
    condition = fields.Text('Condition', required=True, default="True",
        help="Python expression to decide whether the activity can be executed, otherwise it will be deleted or cancelled."
        "The expression may use the following [browsable] variables:\n"
        "   - activity: the funnel activity\n"
        "   - workitem: the funnel workitem\n"
        "   - resource: the resource object this funnel item represents\n"
        "   - transitions: list of funnel transitions outgoing from this activity\n"
        "...- re: Python regular expression module")
    action_type = fields.Selection([('email','Email'), ('action', 'Custom Action')], default='email',
    help="The type of action to execute when an item enters this activity, such as:\n"
             "- Email: send an email using a predefined email template \n"
             "- Report: print an existing Report defined on the resource item and save it into a specific directory \n"
             "- Custom Action: execute a predefined action, e.g. to modify the fields of the resource record")
    email_template_id = fields.Many2one('mail.template', 'Email Template', help='The email to send when this activity is activated')
    server_action_id = fields.Many2one('ir.actions.server', string='Action', help='The action to perform when this activity is activated')
    page_id = fields.Many2one('funnel.page', string="Page")
    to_ids = fields.One2many('funnel.transition', 'activity_from_id', 'Next Activities')
    from_ids = fields.One2many('funnel.transition', 'activity_to_id', 'Previous Activities')
    signal = fields.Char('Signal',
        help="An activity with a signal can be called programmatically. Be careful, the workitem is always created when "
             "a signal is sent")
    keep_if_condition_not_met = fields.Boolean("Don't Delete Workitems", default=False,
        help="By activating this option, workitems that aren't executed because the condition is not met are marked as "
             "cancelled instead of being deleted.")
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)  

class FunnelTransition(models.Model):
    _name = "funnel.transition"
    _description = "Funnel Transition"

    name = fields.Char(compute='_compute_name', string='Name')
    activity_from_id = fields.Many2one('funnel.activity', 'Previous Activity', index=1, required=True, ondelete="cascade")
    activity_to_id = fields.Many2one('funnel.activity', 'Next Activity', required=True, ondelete="cascade")
    interval_nbr = fields.Integer('Interval Value', required=True, default=1)
    interval_type = fields.Selection([('hours', 'Hour(s)'),('days', 'Day(s)'),('months', 'Month(s)'),('years', 'Year(s)')], 'Interval Unit', required=True, default='days')
    trigger = fields.Selection([
        ('auto', 'Automatic'),
        ('time', 'Time'),
        ('cosmetic', 'Cosmetic'),  # fake plastic transition
        ], 'Trigger', required=True, default='time',
        help="How is the destination workitem triggered")
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)  

    _sql_constraints = [
        ('interval_positive', 'CHECK(interval_nbr >= 0)', 'The interval must be positive or zero')
    ]


class FunnelWorkitem(models.Model):
    _name = "funnel.workitem"
    _description = "Funnel Workitem"

    activity_id = fields.Many2one('marketing.campaign.activity', 'Activity', required=True, readonly=True)
    object_id = fields.Many2one('ir.model', string='Resource', index=1, readonly=True, store=True)
    res_id = fields.Integer('Resource ID', index=1, readonly=True)
    res_name = fields.Char(compute='_compute_res_name', string='Resource Name', search='_search_res_name')
    date = fields.Datetime('Execution Date', readonly=True, default=False,
        help='If date is not set, this workitem has to be run manually')
    partner_id = fields.Many2one('res.partner', 'Partner', index=1, readonly=True)
    state = fields.Selection([
        ('todo', 'To Do'),
        ('cancelled', 'Cancelled'),
        ('exception', 'Exception'),
        ('done', 'Done'),
        ], 'Status', readonly=True, copy=False, default='todo')
    error_msg = fields.Text('Error Message', readonly=True)

    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company) 

    def _compute_res_name(self):
        for workitem in self:
            proxy = self.env[workitem.object_id.model]
            record = proxy.browse(workitem.res_id)
            if not workitem.res_id or not record.exists():
                workitem.res_name = '/'
                continue
            workitem.res_name = record.name_get()[0][1] 
    

    
   