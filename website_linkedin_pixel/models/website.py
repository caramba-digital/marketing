# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#


from odoo import api, fields, models, _


class Website(models.Model):
    _inherit = 'website'


    linkedin_pixel = fields.Char('Linkedin Pixel Id')