# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#

from dateutil.relativedelta import relativedelta
from traceback import format_exception
from sys import exc_info
import re
from datetime import datetime
import random
import json

from odoo import api, models, fields, _
from odoo.addons.http_routing.models.ir_http import slug
from odoo.tools.translate import html_translate
from odoo.tools import html2plaintext
from odoo.exceptions import UserError, ValidationError
from odoo.tools.safe_eval import safe_eval

import logging
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
    object_id = fields.Many2one('ir.model', 'Resource', required=True, domain=[('model','in',['res.partner', 'sale.order','crm.lead','event.registration','website.visitor', 'mailing.contact'])],
        help="Choose the resource on which you want this Funnel to be run")
    color = fields.Integer('Kanban Color Index')
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
            funnel_page.website_url = "/touchpoint/%s/page/%s" % (slug(funnel_page.funnel_id), slug(funnel_page))



    name = fields.Char('Page Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', help="Determine the display order", index=True)
    funnel_id = fields.Many2one('funnel.funnel', 'Funnel', required=True, ondelete='cascade')
    object_id = fields.Many2one(related='funnel_id.object_id', relation='ir.model', string='Object', readonly=True)
    type_id = fields.Many2one('funnel.page.type', required=True)
    active = fields.Boolean('Active', default=True)
    content = fields.Html('Content', default=_default_content, translate=html_translate, sanitize=False)
    product_id = fields.Many2one(
        'product.product', string='Product', domain="[('sale_ok', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        change_default=True, ondelete='restrict', check_company=True) 
    product_ids = fields.Many2many('product.product', domain="[('sale_ok', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]" )
    products_ids= fields.Many2many(comodel_name='product.product', string='Products', ondelete='restrict', check_company=True)
    event_id = fields.Many2one('event.event')
    mailing_list_id = fields.Many2one('mailing.list', string='')
    activity_ids = fields.One2many('funnel.activity', 'page_id', 'Activities')
    last_date = fields.Datetime('Last View')
    visits = fields.Integer('No of Views', copy=False, readonly=True)
    is_published = fields.Boolean(default=False)
    website_id = fields.Many2one(related='funnel_id.website_id', readonly=True)
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company) 

    def process_activities(self, object_id, res_id):
        Workitems = self.env['funnel.workitem']
        Activities = self.env['funnel.activity']
        action_date = fields.Datetime.now()
        activity_ids = Activities.search([('start', '=', True), ('page_id', '=', self.id)]).ids
        wi_vals = {
            'date': action_date,
            'state': 'todo',
            'res_id': res_id
        }
        for activity_id in activity_ids:
            wi_vals['activity_id'] = activity_id
            wi = Workitems.create(wi_vals)
            wi.process()
        return True



class FunnelActivity(models.Model):
    _name = 'funnel.activity'
    _description = 'Funnel Activity' 

    name = fields.Char('Name', required=True, translate=True)
    page_id = fields.Many2one('funnel.page', string="Page", required=True, ondelete='cascade', index=True)
    res_id = fields.Integer()
    object_id = fields.Many2one(related='page_id.object_id', relation='ir.model', string='Object', readonly=True)
    start = fields.Integer('Start', help="This activity is launched when the page is viewed.", compute='_compute_start', index=True, store=True)
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
    email_template_id = fields.Many2one('mail.template', 'Email Template', help='The email to send when this activity is activated', domain=[('is_for_funnel', '=', True)])
    server_action_id = fields.Many2one('ir.actions.server', string='Action', help='The action to perform when this activity is activated') 
    to_ids = fields.One2many('funnel.transition', 'activity_from_id', 'Next Activities')
    from_ids = fields.One2many('funnel.transition', 'activity_to_id', 'Previous Activities')
    signal = fields.Char('Signal',
        help="An activity with a signal can be called programmatically. Be careful, the workitem is always created when "
             "a signal is sent")
    keep_if_condition_not_met = fields.Boolean("Don't Delete Workitems", default=False,
        help="By activating this option, workitems that aren't executed because the condition is not met are marked as "
             "cancelled instead of being deleted.")
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company) 

    @api.depends('from_ids')
    def _compute_start(self):
        i = len(self.from_ids.ids)
        return i
    
    def _process_wi_email(self, workitem):
        self.ensure_one()
        return self.email_template_id.send_mail(workitem.partner_id)

    def _process_wi_action(self, workitem):
        self.ensure_one()
        return self.server_action_id.run()



    def process(self, workitem):
        self.ensure_one()
        method = '_process_wi_%s' % (self.action_type,)
        action = getattr(self, method, None)
        if not action:
            raise NotImplementedError('Method %r is not implemented on %r object.' % (method, self._name))
        return action(workitem)




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

    def _compute_name(self):
        # name formatters that depend on trigger
        formatters = {
            'auto': _('Automatic transition'),
            'time': _('After %(interval_nbr)d %(interval_type)s'),
            'cosmetic': _('Cosmetic'),
        }
        # get the translations of the values of selection field 'interval_type'
        model_fields = self.fields_get(['interval_type'])
        interval_type_selection = dict(model_fields['interval_type']['selection'])

        for transition in self:
            values = {
                'interval_nbr': transition.interval_nbr,
                'interval_type': interval_type_selection.get(transition.interval_type, ''),
            }
            transition.name = formatters[transition.trigger] % values

    @api.constrains('activity_from_id', 'activity_to_id')
    def _check_page(self):
        if self.filtered(lambda transition: transition.activity_from_id.page_id != transition.activity_to_id.page_id):
            return ValidationError(_('The To/From Activity of transition must be of the same Page'))

    def _delta(self):
        self.ensure_one()
        if self.trigger != 'time':
            raise ValueError('Delta is only relevant for timed transition.')
        return relativedelta(**{str(self.interval_type): self.interval_nbr})






class FunnelWorkitem(models.Model):
    _name = "funnel.workitem"
    _description = "Funnel Workitem"

    activity_id = fields.Many2one('funnel.activity', 'Activity', required=True, readonly=True)
    object_id = fields.Many2one('ir.model', related='activity_id.page_id.object_id', string='Resource', index=1, readonly=True, store=True)
    res_id = fields.Integer('Resource ID', index=1, readonly=True)
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


    def _process_one(self):
        self.ensure_one()
        if self.state != 'todo':
            return False
        activity = self.activity_id
        resource = self.partner_id
        eval_context = {
            'activity': activity,
            'workitem': self,
            'object': resource,
            'resource': resource,
            'transitions': activity.to_ids,
            're': re,
        }
        try:
            condition = activity.condition
            if condition:
                if not safe_eval(condition, eval_context):
                    if activity.keep_if_condition_not_met:
                        self.write({'state': 'cancelled'})
                    else:
                        self.unlink()
                    return
            result = True
            values = {'state': 'done'}
            if not self.date:
                values['date'] = fields.Datetime.now()
            self.write(values)
            if result:
                self.refresh()  # reload
                execution_date = fields.Datetime.from_string(self.date)
                for transition in activity.to_ids:
                    if transition.trigger == 'cosmetic':
                        continue
                    launch_date = False
                    if transition.trigger == 'auto':
                        launch_date = execution_date
                    elif transition.trigger == 'time':
                        launch_date = execution_date + transition._delta()
                    if launch_date:
                        launch_date = fields.Datetime.to_string(launch_date)
                    # Create workitem
                    values = {
                        'date': launch_date,
                        'activity_id': transition.activity_to_id.id,
                        'partner_id': self.partner_id.id,
                        'state': 'todo',
                    }
                    workitem = self.create(values)
                    if  transition.trigger == 'auto':
                        workitem._process_one()
        except Exception:    
            tb = "".join(format_exception(*exc_info()))
            self.write({'state': 'exception', 'error_msg': tb})


    def process(self):
        for workitem in self:
            workitem._process_one()
        return True

    @api.model
    def run(self, autocommit=False):
        while True:
            workitems = self.search([('done', '=', False), ('date', '!=', False), ('scheduled_date', '<=', datetime.strftime(fields.datetime.now(), tools.DEFAULT_SERVER_DATETIME_FORMAT))])
            if not workitems:
                break
            workitems.process()
        return True

    
    def button_cancel(self):
        return self.filtered(lambda workitem: workitem.state in ('todo', 'exception')).write({'state': 'cancelled'})

    def button_draft(self):
        return self.filtered(lambda workitem: workitem.state in ('exception', 'cancelled')).write({'state': 'todo'})

    def preview(self):
        self.ensure_one()
        res = {}
        if self.activity_id.action_type == 'email':
            view_ref = self.env.ref('mail.email_template_preview_form')
            res = {
                'name': _('Email Preview'),
                'view_type': 'form',
                'view_mode': 'form,tree',
                'res_model': 'email_template.preview',
                'view_id': False,
                'context': self.env.context,
                'views': [(view_ref and view_ref.id or False, 'form')],
                'type': 'ir.actions.act_window',
                'target': 'new',
                'context': "{'template_id': %d,'default_res_id': %d}" % (self.activity_id.email_template_id.id, self.partner_id)
            }

        else:
            raise UserError(_('The current step for this item has no email to preview.'))
        return res


    
   