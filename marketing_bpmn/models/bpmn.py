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

class BpmnDefinitions(models.Model):
    _name = 'bpmn.definitions'
    _description = 'BPMN Definitions'
    _inherit = ['mail.thread', 'mail.activity.mixin','image.mixin']

    name = fields.Char('Name', required=True, translate=True, default='bpmn')
    bpmn_id = fields.Char('BPMN Id', required=True, readonly=True)
    description = fields.Text('Description')
    collaborations_ids = fields.One2many('bpmn.collaboration', 'definitions_id', string='Pools')
    process_ids = fields.One2many('bpmn.process', 'definitions_id', string='Process')
    diagrams_ids = fields.One2many('bpmn.diagram', 'definitions_id', string='Diagrams')
    exporter = fields.Char(required=True,  default='bpmn-js (https://demo.bpmn.io)', readonly=True)
    exporter_version = fields.Char(required=True,  default='8.0.1', readonly=True)
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)

class BpmnDiagram(models.Model):
    _name = 'bpmn.diagram'
    _description = 'BPMN Diagram'

    name = fields.Char('Name', required=True, translate=True)
    bpmn_id = fields.Char('BPMN Id', required=True, readonly=True)
    planes_ids = fields.One2many('bpmn.plane', 'diagram_id', string='Planes')
    definitions_id = fields.Many2one('bpmn.definitions', string='BPMN2 Model', required=True)
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)

class BpmnPlane(models.Model):
    _name = 'bpmn.plane'
    _description = 'BPMN Plane'

    name = fields.Char('Name', required=True, translate=True)
    bpmn_id = fields.Char('BPMN Id', required=True, readonly=True)
    bpmn_element = fields.Char(string='bpmnElement', required=True, readonly=True)
    diagram_id = fields.Many2one('bpmn.diagram', string='BPMN2 Model', required=True)
    shapes_ids = fields.One2many('bpmn.shape', 'plane_id', string='Shapes')
    edges_ids_name = fields.One2many('bpmn.edge', 'plane_id', string='Diagrams')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)

class BpmnShape(models.Model):
    _name = 'bpmn.shape'
    _description = 'BPMN Shape'

    name = fields.Char('Name', required=True, translate=True)
    bpmn_id = fields.Char('BPMN Id', required=True, readonly=True)
    bpmn_element = fields.Char(string='bpmnElement', required=True, readonly=True)
    is_horizontal = fields.Boolean(string='isHorizontal', default=False, readonly=False)
    x = fields.Integer(string='x', required=True, readonly=True)
    y = fields.Integer(string='y', required=True, readonly=True)
    width = fields.Integer(string='Width', required=True, readonly=True)
    height = fields.Integer(string='Height', required=True, readonly=True)
    plane_id = fields.Many2one('bpmn.plane', string='Plane', required=True)
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)

class BpmnEdge(models.Model):
    _name = 'bpmn.edge'
    _description = 'BPMN Edge'

    name = fields.Char('Name', required=True, translate=True)
    bpmn_id = fields.Char('BPMN Id', required=True, readonly=True)
    x1 = fields.Integer(string='x', required=True, readonly=True)
    y1 = fields.Integer(string='y', required=True, readonly=True)
    x2 = fields.Integer(string='x', required=True, readonly=True)
    y2 = fields.Integer(string='y', required=True, readonly=True)
    plane_id = fields.Many2one('bpmn.plane', string='Plane', required=True)
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)


class BpmnCollaboration(models.Model):
    _name = 'bpmn.collaboration'
    _description = 'BPMN Collaboration'

    name = fields.Char('Name', required=True, translate=True, default='bpmn')
    bpmn_id = fields.Char('BPMN Id', required=True)
    definitions_id = fields.Many2one('bpmn.definitions', string='BPMN2 Model', required=True)
    participants_ids = fields.One2many('bpmn.participant', 'collaboration_id', string='Pools')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company) 


class BpmnParticipant(models.Model):
    _name = 'bpmn.participant'
    _description = 'BPMN Pool'

    name = fields.Char('Name',translate=True)
    bpmn_id = fields.Char('BPMN Id', required=True, readonly=True)
    process_ref = fields.Char('processRef')
    collaboration_id = fields.Many2one('bpmn.collaboration', string='Collaboration')
    proces_id = fields.Many2one('bpmn.process', string='Process')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company) 

class BpmnProcess(models.Model):
    _name = 'bpmn.process'
    _description = 'BPMN Process'

    name = fields.Char('Name', required=True, translate=True)
    bpmn_id = fields.Char('BPMN Id', required=True, readonly=True)
    is_executable = fields.Boolean('isExecutable')
    definitions_id = fields.Many2one('bpmn.definitions', string='BPMN2 Model', required=True)
    lane_sets_ids = fields.One2many('bpmn.lane_set', 'process_id', string='Process')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company) 

class BpmnLaneSet(models.Model):
    _name = 'bpmn.lane_set'
    _description = 'BPMN Process'

    bpmn_id = fields.Char('BPMN Id', required=True, readonly=True)
    process_id = fields.Many2one('bpmn.process', string='Process')
    lanes_ids = fields.One2many('bpmn.lane', 'lane_set_id', string='Lanes')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company) 


class BpmnLane(models.Model):
    _name = 'bpmn.lane'
    _description = 'BPMN Lane'

    name = fields.Char('Name', required=True, translate=True)
    bpmn_id = fields.Char('BPMN Id', required=True, readonly=True)
    lane_set_id = fields.Many2one('bpmn.lane_set', string='Lane Set')
    flow_node_ref_ids = fields.One2many('bpmn.flow_node_ref', 'lane__id', string='Object Reference')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)


class BpmnFlowNodeRef(models.Model):
    _name = 'bpmn.flow_node_ref'
    _description = 'BPMN Flow Node Ref'

    bpmn_ref = fields.Char('Ref', required=True)
    lane_id = fields.Many2one('bpmn.lane')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)

class BpmnTask(models.Model):
    _name = 'bpmn.task'
    _description = 'BPMN Task' 

    name = fields.Char('Name', required=True, translate=True)
    bpmn_id = fields.Char('BPMN Id', required=True, readonly=True)
    process_id = fields.Many2one('bpmn.process', string='Process')
    task_type = fields.Selection([
        ('task','Task'),
        ('sendTask','Send Task'),
        ('recibeTask','Receive Task'),
        ('userTask','User Task'),
        ('manualTask','Manual Task'),
        ('businessTask','Business Rule Task'),
        ('serviceTask','Service Task'),
        ('scriptTask','Script Task'),
    ], string='Task Type', default='task', required=True)
    res_id = fields.Integer()
    object_id = fields.Many2one('ir.model', string='Object', readonly=True)
    email_template_id = fields.Many2one('mail.template', 'Email Template', help='The email to send when this activity is activated', domain=[('is_for_bpmn', '=', True)])
    server_action_id = fields.Many2one('ir.actions.server', string='Action', help='The action to perform when this activity is activated') 
    incoming = fields.Char()
    outgoing = fields.Char()
    from_id = fields.Many2one('bpmn.task', string='Previous Task')
    from_gateway_id = fields.Many2one('bpmn.gateway', string='Previous Gateway')
    from_event_id = fields.Many2one('bpmn.event', string='Previous Event')
    to_id  = fields.Many2one('bpmn.task', string='Next Task')
    to_gateway_id = fields.Many2one('bpmn.gateway', string='Next Gateway')
    to_event_id = fields.Many2one('bpmn.event', string='Next Event')
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
    bpmn_id = fields.Char('BPMN Id', required=True, readonly=True)
    process_id = fields.Many2one('bpmn.process', string='Process')
    gateway_type = fields.Selection([
        ('exclusiveGateway','Exclusive Gateway'),
        ('parallelGateway','Parallel Gateway'),
        ('inclusiveGateway','Inclusive Gateway'),
        ('complexGateway','Complex Gateway'),
        ('eventBasedGateway','Event based Gateway')])
    from_id = fields.One2many('bpmn.task', 'to_gateway_id', string='Previous Task')
    from_gateway_id = fields.One2many('bpmn.gateway', 'to_gateway_id', string='Previous Gateway')
    from_event_id = fields.One2many('bpmn.event', 'to_gateway_id', string='Previous Event')
    to_id  = fields.One2many('bpmn.task', 'from_gateway_id', string='Next Task')
    to_gateway_id = fields.One2many('bpmn.gateway', 'from_gateway_id', string='Next Gateway')
    to_event_id = fields.One2many('bpmn.event', 'from_gateway_id', string='Next Event')
    fields_lines = fields.One2many('ir.server.object.lines', 'server_id', string='Value Mapping', copy=True)
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company) 


class BpmnEvent(models.Model):
    _name = 'bpmn.event'
    _description = 'BPMN Event' 

    name =  fields.Char('Name', required=True, translate=True)
    bpmn_id = fields.Char('BPMN Id', required=True, readonly=True)
    process_id = fields.Many2one('bpmn.process', string='Process')
    event_model = fields.Selection([('start_event','Start'),('start_event_sub_process','Start Sub Process'),('intermediate_event',''),('boundary_event',''),('end_event','')], string='BPMN Model')  
    event_type = fields.Selection([
        ('startEvent','Start Event'),
        ('intermediateThrowEvent','Intermediate Throw Event'),
        ('endEvent','End Event'),
        ('messageEventDefinition','Message Intermediate Catch Event'),
        ('timerEventDefinition','Timer Intermediate Catch Event'),
        ('escalationEventDefinition','Escalation Intermediate Throw Event'),
        ('errorEventDefinition','Error End Event'),
        ('cancelEventDefinition','Cancel End Event'),
        ('conditionalEventDefinition','Conditional Intermediate Catch Event'),
        ('linkEventDefinition','Link Intermediate Catch Event'),
        ('linkEventDefinition','Link Intermediate Throw Event'),
        ('compensateEventDefinition','Compensation Intermediate Throw Event'),
        ('terminateEventDefinition','Terminate End Event'),
        ('signalEventDefinition','Signal Intermediate Throw Event')], string='Type')
    from_id = fields.Many2one('bpmn.task', string='Previous Task')
    from_gateway_id = fields.Many2one('bpmn.gateway', string='Previous Gateway')
    from_event_id = fields.Many2one('bpmn.event', string='Previous Event')
    to_id  = fields.Many2one('bpmn.task', string='Next Task')
    to_gateway_id = fields.Many2one('bpmn.gateway', string='Next Gateway')
    to_event_id = fields.Many2one('bpmn.event', string='Next Event')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company) 




class BpmnSequenceFlow(models.Model):
    _name = 'bpmn.sequence_flow'
    _description = 'BPMN Sequence Flow' 

    bpmn_id = fields.Char('BPMN Id', required=True, readonly=True)
    process_id = fields.Many2one('bpmn.process', string='Process')
    source_ref = fields.Char(string='sourceRef')
    target_ref = fields.Char(string='targetRef')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company) 

class BpmnWorkitem(models.Model):
    _name = "bpmn.workitem"
    _description = "BPMN Workitem"

    task_id = fields.Many2one('bpmn.task', 'Task', required=True, readonly=True)
    object_id = fields.Many2one('ir.model', string='Resource', index=1, readonly=True, store=True)
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
