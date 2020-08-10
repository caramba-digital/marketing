# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#

from odoo import api, fields, models, tools, _

class MarketingStrategyStoryBrandTheme(models.Mosel):
    _name = "marketing_strategy.story_brand.theme"
    _description = "Story Brand Theme"

    name = fields.Char('Name', required=True)
    description = fields.Char()
    concept = fields.Html()
    contents_ids = fields.One2many('marketing_strategy.story_brand.content', 'theme_id') 
    


class MarketingStoryBrandContent(models.Model):
    _name = "marketing_strategy.story_brand.content"
    _description = "Story Brand Content"

    name = fields.Char('Name', required=True)
    content_type = fields.Selection([('help','Help Content'),('hub','Hub Content'),('hero','Hero Content')])
    value = fields.Selection([('inspire','Inspire'),('educate','Educate'),('entertain','Entertain')])
    mode = fields.Selection([('search','Search'),('display','Display'),('organic','Organic'), ('opt_in','Opt-in')])
    format = fields.Selection([('blog','Blog'),('longform_content','Longform Content'),('case_study','Case Study'),('white_paper','White Paper'),('ebook','Ebook'),('infographic','Infographic'),('survey','Survey'),('video','Video'),('short_video','Short Video'),('webinar','Webinar'),('online_curse','Online Course'),('email','email')])
    theme_id = fields.Many2one('marketing_strategy.story_brand.theme')
