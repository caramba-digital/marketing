# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Challenge(models.Model):
    _inherit = 'gamification.challenge'

    category = fields.Selection(selection_add=[('funnel', 'Marketing / Forum')])


class GamificationBadgeUser(models.Model):
    """User having received a badge"""
    _inherit = 'gamification.badge.user'

    client_id = fields.Many2one('res.partner', string='Client', domain=[()])




class GamificationBadge(models.Model):
    _inherit = 'gamification.badge'

    granted_client_count = fields.Integer(compute="_compute_granted_clients_count")

    @api.depends('owner_ids.employee_id')
    def _compute_granted_employees_count(self):
        for badge in self:
            badge.granted_client_count = self.env['gamification.badge.user'].search_count([
                ('badge_id', '=', badge.id),
                ('employee_id', '!=', False)
            ])

    def get_granted_clients(self):
        employee_ids = self.mapped('owner_ids.employee_id').ids
        return {
            'type': 'ir.actions.act_window',
            'name': 'Granted Employees',
            'view_mode': 'kanban,tree,form',
            'res_model': 'hr.employee.public',
            'domain': [('id', 'in', employee_ids)]
        }