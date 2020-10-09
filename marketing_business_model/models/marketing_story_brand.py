# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#
from odoo import api, fields, models

class MarketingStrategyStoryBrandContent(models.Model):
   _inherit = "marketing_strategy.story_brand.content"

   channel_id = fields.Many2one('marketing_strategy.channel')
