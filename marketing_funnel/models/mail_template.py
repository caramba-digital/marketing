# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#

from odoo import api, fields, models


class MailTemplate(models.Model):
    _inherit = "mail.template"

    is_for_funnel = fields.Boolean('Is For Funnel', default=False)
    
        
    