# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#

from odoo import api, fields, models, tools, _

class MarketingStrategyStoryBrandTheme(models.Model):
    _name = "marketing_strategy.story_brand.theme"
    _description = "Story Brand Theme"

    name = fields.Char('Name', required=True)
    description = fields.Char()
    content_type = fields.Selection([('help','Help Content'),('hub','Hub Content'),('hero','Hero Content')])
    value = fields.Selection([('inspire','Inspire'),('educate','Educate'),('entertain','Entertain')])
    concept = fields.Html()
    contents_ids = fields.One2many('marketing_strategy.story_brand.content', 'theme_id')
    story_brand_id = fields.Many2one('marketing_strategy.story_brand') 
    


class MarketingStrategyStoryBrandContent(models.Model):
    _name = "marketing_strategy.story_brand.content"
    _description = "Story Brand Content"

    name = fields.Char('Name', required=True)
    content = fields.Html()
    mode = fields.Selection([('search','Search'),('display','Display'),('organic','Organic'), ('opt_in','Opt-in')])
    format = fields.Selection([('blog','Blog'),('longform_content','Longform Content'),('case_study','Case Study'),('white_paper','White Paper'),('ebook','Ebook'),('infographic','Infographic'),('survey','Survey'),('video','Video'),('short_video','Short Video'),('webinar','Webinar'),('online_curse','Online Course'),('email','email')])
    theme_id = fields.Many2one('marketing_strategy.story_brand.theme')
    touch_point_ids = fields.Many2many('marketing_strategy.touchpoint', 'marketing_strategy_content_touchpoint_rel', 'touchpoint_id', 'content_id')
    


class MarketingStrategyStoryBrand(models.Model):
    _name = "marketing_strategy.story_brand"
    _description = "Story Brand"

    name = fields.Char('Name', required=True)
    summary = fields.Html()
    brand_owner_id = fields.Many2one('res.partner', required=True)
    value_proposition_id = fields.Many2one('marketing_strategy.value_proposition', required=True)
    user_id = fields.Many2one('res.users', string='Responsible', default=lambda self: self.env.user, track_visibility="onchange")
    brand_id = fields.Many2one('marketing_strategy.brand', domain = [('relation','=', 'main')], string='Mentor', required=True)
    buyers_id = fields.Many2many('marketing_strategy.buyer_persona', 'Heroes')    
    chapter_1 = fields.One2many('marketing_strategy.story_brand.theme', 'story_brand_id', string="Status Quo", help="The hero is introduced in their ordinary world. Complacent, but lacking something.")
    chapter_2 = fields.One2many('marketing_strategy.story_brand.theme', 'story_brand_id', string="Call to Adventure", help="The hero is called to go out and achieve the thing she wants the most.")
    chapter_3 = fields.One2many('marketing_strategy.story_brand.theme', 'story_brand_id', string="Refusal of the call", help="But the hero scared of change and ignores her calling.")
    chapter_4 = fields.One2many('marketing_strategy.story_brand.theme', 'story_brand_id', string="Meeting with the mentor", help="The hero meets a sage or is given a special tool that convinces her that she can succeed.")
    chapter_5 = fields.One2many('marketing_strategy.story_brand.theme', 'story_brand_id', string="Crossing the threshold", help="The hero enters the adventure to a point of no return.")
    chapter_6 = fields.One2many('marketing_strategy.story_brand.theme', 'story_brand_id', string="Trials and Allies", help="The hero undergoes tests and makes new friends all in a montage that trains her to overcome the biggest test yet to come.")
    chapter_7 = fields.One2many('marketing_strategy.story_brand.theme', 'story_brand_id', string="Approaching the cave", help="The hero is ready to face her biggest fear.")
    chapter_8 = fields.One2many('marketing_strategy.story_brand.theme', 'story_brand_id', string="The Ordeal", help="The hero faces the biggest fear and, whether successful or not, gains something and loses something in return.")
    chapter_9 = fields.One2many('marketing_strategy.story_brand.theme', 'story_brand_id', string="The Reward", help="The hero receives some kind of reward for facing her fears.")
    chapter_10 = fields.One2many('marketing_strategy.story_brand.theme', 'story_brand_id', string="The Road Back", help="The hero crosses the threshold to return to the ordinary world, but is being chased by the unresolved conflict with her fears.")
    chapter_11 = fields.One2many('marketing_strategy.story_brand.theme', 'story_brand_id', string="Resurrection", help="The threat is at its highest and the hero pulls out all of the knowledge and skills that she gained earlier in her trials, reaching into the darkest depths of herself and transcending into a more powerful version of herself.")
    chapter_12 = fields.One2many('marketing_strategy.story_brand.theme', 'story_brand_id', string="Return with the Elixir", help="After defeating the big bad, the hero returns to her ordinary life, having changed and now with the ability to share her new knowledge with the world.")
