# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Challenge(models.Model):
    _inherit = 'gamification.challenge'

    challenge_category = fields.Selection(selection_add=[('marketing', 'Marketing / Strategy')], ondelete={'marketing': 'set default'})



class GamificationBadgeUser(models.Model):
    _inherit = 'gamification.badge.user'

    is_client = fields.Boolean('Is Client', default=False)



class GamificationBadge(models.Model):
    _inherit = 'gamification.badge'

    granted_clients_count = fields.Integer(compute="_compute_granted_clients_count")
    is_for_clients = fields.Boolean('Is for clients', Default=False)

    def _compute_granted_clients_count(self):
        for badge in self:
            badge.granted_clients_count = self.env['gamification.badge.user'].search_count([
                ('badge_id', '=', badge.id),
                ('is_client', '=', True)
            ])

    def get_granted_cliets(self):
        domain = [('is_client','=',True),('badge_id','=',self.id)]
        records = self.env['gamification.badge.user'].search(domain)
        client_ids = records.mapped('user_id')
        return {
            'type': 'ir.actions.act_window',
            'name': 'Granted Clients',
            'view_mode': 'kanban,tree,form',
            'res_model': 'res.users',
            'domain': [('id', 'in', client_ids)]
        }

