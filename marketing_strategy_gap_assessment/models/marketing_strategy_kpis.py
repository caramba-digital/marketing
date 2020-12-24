# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#

from odoo import api, fields, models, tools, _

class MarketingBrandKpisTracking(models.Model):
    _name = 'marketing_strategy.brand_kpis_tracking'
    _order = 'create_date'

    twitter_folowers = fields.Integer('Folowers')
    facebook_likes = fields.Integer('Likes')
    facebook_folowers = fields.Integer('Folowers')
    instagram_posts = fields.Integer('Posts')
    instagram_folowers = fields.Integer('Folowers')
    linkedin_folowers = fields.Integer('Folowers')
    youtube_subscribers = fields.Integer('Subscribers') 
    tiktok_folowers = fields.Integer('Folowers')
    tiktok_likes = fields.Integer('Likes') 
    url = fields.Char('Website')
    podcast_rank = fields.Integer('Rank')
    podcast_episodes = fields.Integer('Episodes')
    
    brand_id = fields.Many2one('marketing_strategy.brand')




class MarketingPlanKpisTracking(models.Model):
    _name = 'marketing_strategy.plan_kpis_tracking'
    _order = 'create_date'

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
    tiktok_folowers = fields.Integer()
    tiktok_likes = fields.Integer()
    #consideration
    shopping_cart_viewed = fields.Integer()
    abandoned_shopping_cart = fields.Integer()
    leads = fields.Integer()
    leads_lost = fields.Integer()
    leads_won = fields.Integer()
    quotations = fields.Integer()
    quoted_amount = fields.Monetary()
    #purchase
    revenue_per_visitor = fields.Monetary()
    sales = fields.Integer()    
    sales_amount = fields.Monetary()
    new_customers = fields.Integer()
    new_customers_amount = fields.Monetary()    
    customer_acquisition_cost = fields.Float()
    #service  
    sales_canceled = fields.Integer() 
    sales_canceled_amount = fields.Monetary() 
    net_promoter_score = fields.Float()
    #loyalty
    recurring_customers = fields.Integer()
    recurring_customers_amount = fields.Monetary()
    customer_lifetime_value = fields.Monetary()
    recommendations = fields.Integer()
    #reputation
    mentions = fields.Integer()
    evangelists = fields.Integer()
    haters = fields.Integer()
    brand_sentiment = fields.selection([('negative','Negative'),('neutral','Neutral'),('positive','Positive')])
    #master
    ltv = fields.Monetary('Life Time Value')
    cac = fields.Monetary('Customer Acquisition Cost')
    ltv_cac = fields.Monetary('LTV:CAC')
    aov = fields.Monetary('Average Order Value')
    net_income = fields.Monetary() 
    Investment = fields.Monetary()
    roas = fields.Monetary('ROAS', help='Return on Ad Spend')
    roi = fields.Monetary('ROI', help='Return on Investment')
    plan_id = fields.Many2one('marketing_strategy.plan_tracking')



class Plan(models.Model):
    _name = 'marketing_strategy.plan'
    _inherit  = ['marketing_strategy.plan']


    planning_period = fields.Selection([
        ('yearly','Yearly'),
        ('biannual','Biannual'),
        ('quarterly','Quarterly'),
        ('monthly','Monthly'),
        ('weekly','Weekly'),
        ('diary','Diary')
        ], default='monthly')

    kpis_tracking_ids = fields.One2Many('marketing_strategy.plan_kpis_tracking', 'plan_id')




