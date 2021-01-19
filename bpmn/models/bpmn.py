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

class BpmnCollaboration(models.Model):
    _name = 'bpmn.collaboration'
    _description = 'BPMN Collaboration'

    name = fields.Char('Name', required=True, translate=True, default='bpmn')
    bpmn_id = fields.Char('BPMN Id', required=True)
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company) 


class BpmnParticipant(models.Model):
    _mame = 'bpmn.participant'
    _description = 'bpmn.participant'
    _order = 'id'

    name = fields.Char('Name',translate=True)
    bpmn_id = fields.Char('BPMN Id', required=True)
    process_ref = fields.Char('processRef')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company) 


class BpmnProcess(models.Model):
    _name = 'bpmn.process'
    _description = 'BPMN Process'

    name = fields.Char('Name', required=True, translate=True)
    bpmn_id = fields.Char('BPMN Id', required=True)
    is_executable = fields.Boolean('isExecutable')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company) 

class BpmnLaneSet(models.Model):
    _name = 'bpmn.laneset'
    _description = 'BPMN Process'

    bpmn_id = fields.Char('BPMN Id', required=True)


class BpmnLane(models.Model):
    _name = 'bpmn.lane'
    _description = 'BPMN Lane'

    name = fields.Char('Name', required=True, translate=True)
    bpmn_id = fields.Char('BPMN Id', required=True)
    flow_mode_ref_ids = fields.One2many('bpmn.flow_mode_ref', 'lane__id')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)


class BpmnFlowNodeRef(models.Model):
    _name = 'bpmn.flow_mode_ref'
    _description = 'BPMN Lane'

    bpmn_id = fields.Char('BPMN Id', required=True)
    lane_id = fields.Many2one('bpmn.lane')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)



class BpmnTask(models.Model):
    _name = 'bpmn.task'
    _description = 'BPMN Task' 

    name = fields.Char('Name', required=True, translate=True)
    task_type = fields.Selection([
        ('task','Task'),
        ('sendTask','Send Task'),
        ('recibeTask','Receive Task'),
        ('userTask','User Task'),
        ('manualTask','Manual Task'),
        ('businessTask','Business Rule Task'),
        ('serviceTask','Service Task'),
        ('scriptTask','Script Task'),
    ]), string='Task Type', default='task', required=True)
    email_template_id = fields.Many2one('mail.template', 'Email Template', help='The email to send when this activity is activated', domain=[('is_for_funnel', '=', True)])
    server_action_id = fields.Many2one('ir.actions.server', string='Action', help='The action to perform when this activity is activated') 
    incoming = fields.Char()
    outgoing = fields.Char()
    from_id = fields.Many2one('funnel.activity', string='Previous Task')
    from_gateway_id = fields.Many2one('funnel.gateway', string='Previous Gateway')
    from_event_id = fields.Many2one('funnel.event', string='Previous Event')
    to_id  = fields.Many2one('funnel.activity', string='Next Task')
    to_gateway_id = fields.Many2one('funnel.gateway', string='Next Gateway')
    to_event_id = fields.Many2one('funnel.event', string='Next Event')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company) 
    
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


class BpmnGateway(models.Model):
    _name = 'bpmn.gateway'
    _description = 'BPMN Gateway' 

    name =  fields.Char('Name', required=True, translate=True)
    gateway_type = fields.Selection([
        ('exclusiveGateway','Exclusive Gateway'),
        ('parallelGateway','Parallel Gateway'),
        ('inclusiveGateway','Inclusive Gateway'),
        ('complexGateway','Complex Gateway'),
        ('eventBasedGateway','Event based Gateway)])
    to_ids = fields.One2many('funnel.activity', 'from_gateway_id', 'Next Activities')
    to_events = fields.One2many('funnel.event', 'from_gateway_id', 'Next Event')
    from_ids = fields.One2many('funnel.activity', 'to_gateway_id', 'Previous Activities')
    from_event_ids = fields.One2many('funnel.event', 'to_gateway_id', 'Previous Events')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company) 

class BpmnStartEvent(models.Model):
    _name = 'bpmn.start_event'
    _description = 'BPMN Start Event' 

    name =  fields.Char('Name', required=True, translate=True)
    event_type = fields.Selection([
        ('startEvent','Start Event'),
        ('intermediateThrowEvent','Intermediate Throw Event'),
        ('endEvent','End Event'),
        ('messageEventDefinition','Message Start Event'),
        ('timerEventDefinition','Timer Start Event'),
        ('conditionalEventDefinition','Conditional Start Event'),
        ('signalEventDefinition','Signal Start Event')], string='Type')
    from_id = fields.Many2one('funnel.activity', string='Previous Activity')
    from_gateway_id = fields.Many2one('funnel.gateway', string='Previous Gateway')
    to_id  = fields.Many2one('funnel.activity', string='Next Activity')
    to_gateway_id = fields.Many2one('funnel.gateway', 'Next Gateway')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company) 


class BpmnStartEventSubProcess(models.Model):
    _name = 'bpmn.start_event_sub_process'
    _description = 'BPMN Start Event Sub Process' 

    name =  fields.Char('Name', required=True, translate=True)
    event_type = fields.Selection([
        ('startEvent','Start Event'),
        ('intermediateThrowEvent','Intermediate Throw Event'),
        ('endEvent','End Event')], string='Type')
    from_gateway_id = fields.Many2one('funnel.gateway', string='Previous Gateway')
    to_id  = fields.Many2one('funnel.activity', string='Next Activity')
    to_gateway_id = fields.Many2one('funnel.gateway', 'Next Gateway')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company) 

class BpmnIntermediateEvent(models.Model):
    _name = 'bpmn.intermediate_event'
    _description = 'BPMN Event' 

    name =  fields.Char('Name', required=True, translate=True)
    event_type = fields.Selection([
        ('startEvent','Start Event'),
        ('intermediateThrowEvent','Intermediate Throw Event'),
        ('endEvent','End Event'),
        ('messageEventDefinition','Message Intermediate Catch Event'),
        ('messageEventDefinition','Message Intermediate Throw Event'),
        ('timerEventDefinition','Timer Intermediate Catch Event'),
        ('escalationEventDefinition','Escalation Intermediate Throw Event'),
        ('conditionalEventDefinition','Conditional Intermediate Catch Event'),
        ('linkEventDefinition','Link Intermediate Catch Event'),
        ('linkEventDefinition','Link Intermediate Throw Event'),
        ('compensateEventDefinition','Compensation Intermediate Throw Event'),
        ('signalEventDefinition','Signal Intermediate Catch Event'),
        ('signalEventDefinition','Signal Intermediate Throw Event')], string='Type')
    from_gateway_id = fields.Many2one('funnel.gateway', string='Previous Gateway')
    to_id  = fields.Many2one('funnel.activity', string='Next Activity')
    to_gateway_id = fields.Many2one('funnel.gateway', 'Next Gateway')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company) 

class BpmnEndEvent(models.Model):
    _name = 'bpmn.end_event'
    _description = 'BPMN End Event' 

    name =  fields.Char('Name', required=True, translate=True)
    event_type = fields.Selection([
        ('startEvent','Start Event'),
        ('intermediateThrowEvent','Intermediate Throw Event'),
        ('endEvent','End Event'),
        ('endEvent','Message End Event'),
        ('escalationEventDefinition','Escalation End Event'),
        ('errorEventDefinition','Error End Event'),
        ('cancelEventDefinition','Cancel End Event'),
        ('compensateEventDefinition','Compensation End Event'),
        ('signalEventDefinition','Signal End Event'),
        ('terminateEventDefinition','Terminate End Event')], string='Type')
    from_id = fields.Many2one('funnel.activity', string='Previous Activity')
    from_gateway_id = fields.Many2one('funnel.gateway', string='Previous Gateway')
    to_id  = fields.Many2one('funnel.activity', string='Next Activity')
    to_gateway_id = fields.Many2one('funnel.gateway', 'Next Gateway')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)

class BpmnStartEventSubProcess(models.Model):
    _name = 'bpmn.start_event_sub_process'
    _description = 'BPMN Event' 

    name =  fields.Char('Name', required=True, translate=True)
    event_type = fields.Selection([
        ('messageEventDefinition','Message Start Event'),
        ('timerEventDefinition','Timer Start Event'),
        ('conditionalEventDefinition','Conditional Start Event'),
        ('signalEventDefinition','Signal Start Event'),
        ('errorEventDefinition','Error Start Event'),
        ('escalationEventDefinition','Escalation Start Event'),
        ('compensateEventDefinition','Compensation Start Event'),
        ('messageEventDefinition','Message Start Event (non-interrupting)'),
        ('timerEventDefinition','Timer Start Event (non-interrupting)'),
        ('conditionalEventDefinition','Conditional Start Event (non-interrupting)'),
        ('signalEventDefinition','Signal Start Event (non-interrupting)'),
        ('escalationEventDefinition','Escalation Start Event (non-interrupting)')], string='Type')
    from_id = fields.Many2one('funnel.activity', string='Previous Activity')
    from_gateway_id = fields.Many2one('funnel.gateway', string='Previous Gateway')
    to_id  = fields.Many2one('funnel.activity', string='Next Activity')
    to_gateway_id = fields.Many2one('funnel.gateway', 'Next Gateway')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company) 


class BpmnBoundaryEvent(models.Model):
    _name = 'bpmn.boundary_event'
    _description = 'BPMN Boundary Event' 

    name =  fields.Char('Name', required=True, translate=True)
    event_type = fields.Selection([
        ('messageEventDefinition','Message Boundary Event'),
        ('timerEventDefinition','Timer Boundary Event'),
        ('escalationEventDefinition','Escalation Boundary Event'),
        ('conditionalEventDefinition','Conditional Boundary Event'),
        ('errorEventDefinition','Error Boundary Event'),
        ('cancelEventDefinition','Cancel Boundary Event'),
        ('signalEventDefinition','Signal Boundary Event'),
        ('compensateEventDefinition','Compensation Boundary Event'),
        ('messageEventDefinition','Message Boundary Event (non-interrupting)'),
        ('timerEventDefinition','Timer Boundary Event (non-interrupting)'),
        ('escalationEventDefinition','Escalation Boundary Event (non-interrupting)'),        
        ('conditionalEventDefinition','Conditional Boundary Event (non-interrupting)'),
        ('signalEventDefinition','Signal Boundary Event (non-interrupting)')
        ,], string='Type')
    from_id = fields.Many2one('funnel.activity', string='Previous Activity')
    from_gateway_id = fields.Many2one('funnel.gateway', string='Previous Gateway')
    to_id  = fields.Many2one('funnel.activity', string='Next Activity')
    to_gateway_id = ('funnel.gateway', 'Next Gateway')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company) 
