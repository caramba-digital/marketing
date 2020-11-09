# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#
from odoo import api, fields, models


class MarketingStrategyStoryBrandContent(models.Model):
    _name = "marketing_strategy.story_brand.content"
    _inherit =  ["marketing_strategy.story_brand.content"]

    def _expand_states(self, states, domain, order):
        return ['draft', 'copywriting', 'proofreading', 'design', 'seo','publication', 'done']

    state = fields.Selection([
        ('draft','Draft'),
        ('copywriting','Copywriting'),
        ('proofreading','Proofreading'),
        ('design','Design'),
        ('seo','SEO'), 
        ('publication','Publication'), 
        ('done','Done'),
        ('cancel','Cancel')], default='draft', required=True, copy=False, group_expand='_expand_states')
    progress = fields.Float(compute='_compute_progress', readonly=True)
    published_date = fields.Datetime('Published Date')
    content_date = fields.Datetime('Publishing Date')
    calendar_date = fields.Datetime('Scheduled Date')
    owner_id = fields.Many2one('res.users')
    writer_id = fields.Many2one('res.users')

    @api.depends('scheduled_date','published_date')
    def _compute_calendar(self):
        for record in self:
            if record.published_date:
                record.calendar = record.published_date
            else:
                if record.scheduled_date:
                    record.calendar = record.scheduled_date

    @api.depends('state')
    def _compute_progress(self):
        for record in self:
            if self.state=='copywriting':
                progress=20.0
            elif self.state=='proofreading':
                progress=40.0
            elif self.state=='design':
                progress=60.0
            elif self.state=='seo':
                progress=80.0
            elif self.state=='publication':
                progress:90.0
            elif self.state=='done':
                progress=100.0
            else:
                progress=0.0
            record.progress = progress







