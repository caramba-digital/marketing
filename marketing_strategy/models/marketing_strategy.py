# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class MarketingConsumerTrend(models.Model):
    _name = "marketing.consumer_trend"
    _description = "Consumer Trend Canvas"
    
    name: fields.Char('Area Name', required=True, index=True)
    