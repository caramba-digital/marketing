# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#

from odoo import api, fields, models, tools, _
 
class Plan(models.Model):
   _name = 'marketing_strategy.plan'
   _inherit = ['marketing_strategy.plan']
   
   tracking_ids = fields.One2many('marketing_strategy.tracking')


class MarketingTracking(models.Model):
   _name = 'marketing_strategy.tracking'
   _order = 'date'

   date = fields.date()
   parent_id = fields.Many2one('marketing_strategy.tracking')
   #awareness
   website_ranking = fields.Integer()
   website_page_views = fields.Integer()
   website_time_on_page = fields.Time()
   bounce_rate = fields.float()
   facebook_likes = fields.Integer()
   facebook_interactions = fields.Integer()
   facebook_views = fields.Integer()
   twitter_followers = fields.Integer()
   twitter_views = fields.Integer()
   twitter_mentions = fields.Integer()
   instagram_likes = fields.Integer()
   instagram_interactions = fields.Integer()
   instagram_views = fields.Integer()
   youtube_susbscribers = fields.Integer()
   youtube_views = fields.Integer()
   youtube_watch_duration = fields.Time()
   youtube_comments = fields.Integer()
   #consideration
   shopping_cart_viewed = fields.Integer()
   abandoned_shopping_cart = fields.Integer()
   revenue_per_visitor = fields.Monetary()
   leads = fields.Integer()
   leads_lost = fields.Integer()
   leads_won = fields.Integer()
   quotations = fields.Integer()
   quoted_amount = fields.Monetary()
   #purchase
   sales = fields.Integer()    
   sales_amount = fields.Monetary()
   new_customers = fields.Integer()
   new_customers_amount = fields.Monetary()    
   customer_acquisition_cost = fields.Float()
   #service  
   sales_canceled = fields.Integer() 
   sales_canceled_amount = fields.Monetary() 
   net_promoter_score = fields.Float()
   brand_sentiment = fields.selection([('negative','Negative'),('neutral','Neutral'),('positive','Positive')])
   #
   #loyalty
   recurring_customers = fields.Integer()
   recurring_customers_amount = fields.Monetary()
   customer_lifetime_value = fields.Monetary()
   recommendations = fields.Integer()
   evangelists = fields.Integer()
   #master
   ltv_cac = fields.Monetary('LTV:CAC')
   net_income = fields.Monetary() 
   Investment = fields.Monetary()
   roi = fields.Float()

    
    
