# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#

from odoo import api, fields, models


class BlogPost(models.Model):
    _inherit = ['blog.post']

    scheduled_date = fields.Datetime('Scheduled Date')
    theme_id = fields.Many2one('marketing_strategy.story_brand.theme')


