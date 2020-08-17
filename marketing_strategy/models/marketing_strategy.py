# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#

from odoo import api, fields, models, tools, _
 

PRODUCT_TYPE = [('good','Good'), ('service','Service'), ('event','Event'), ('experience','Experiences'), ('','People'), ('pleace','Place'), ('property_right','Property right'), ('institution','Institution'), ('information','Information'), ('idea','Idea')]
PERSONALITY = [('average', 'Average'), ('reserved', 'Reserved'), ('self_centered', 'Self-centered'), ('role_model', 'Role model')]

class BrandTag(models.Model):

    _name = "marketing_strategy.brand.tag"
    _description = "Brand Tag"

    name = fields.Char('Tag Name', required=True, translate=True)
    color = fields.Integer('Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]

class BrandTopic(models.Model):

    _name = "marketing_strategy.brand.topic"
    _description = "Topics of Conversation"

    name = fields.Char('Topics of Conversation', required=True, translate=True)
    color = fields.Integer('Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]

class MarketingNeed(models.Model):

    _name = "marketing_strategy.need"
    _description = "Needs"

    name = fields.Char('Name', required=True, translate=True, readonly=True)


class MarketingValue(models.Model):

    _name = "marketing_strategy.value"
    _description = "Values"

    name = fields.Char('Name', required=True, translate=True, readonly=True)
       
       
class MarketingBrand(models.Model):
    _name = 'marketing_strategy.brand'
    _description = 'Brand'    
    _inherit = ['mail.thread', 'mail.activity.mixin','image.mixin']
    _order = 'name asc'

    def _expand_relation(self, states, domain, order):
        return ['main', 'competitor', 'collaborator', 'family']

    name = fields.Char('Brand', required=True)
    product_type = fields.Selection(PRODUCT_TYPE)
    relation = fields.Selection([('main','Main'),('competitor','Competitor'),('collaborator','Collaborator'),('family','Family')], 
    required=True, default='competitor', group_expand='_expand_relation')
    partner_id = fields.Many2one('res.partner', string='Partner')
    related_brand_id = fields.Many2one('marketing_strategy.brand', string='Related Brand')
    tag_ids = fields.Many2many('marketing_strategy.brand.tag', 'marketing_strategy_brand_tags_rel', 'brand_id', 'tag_id', string='Tags') 
    color = fields.Integer('Kanban Color Index')
    partner_id = fields.Many2one('res.partner', string='Partner')
    twitter = fields.Char('Twitter Account')
    facebook = fields.Char('Facebook Page')
    linkedin = fields.Char('Linkedin Page')
    youtube = fields.Char('Youtube Channel')
    tiktok =  fields.Char('TikTok')
    blog = fields.Char('Blog')
    url = fields.Char('Website')
    podcast_channel = fields.Char('Podcast Channel')
    openness = fields.Float(default=50, readonly=True)
    conscientiousness = fields.Float(default=50, readonly=True)
    extraversion = fields.Float(default=50, readonly=True)
    agreeableness = fields.Float(default=50, readonly=True)
    emotional_range = fields.Float(default=50, readonly=True)
    needs_ids = fields.Many2many('marketing_strategy.need')
    values_ids = fields.Many2many('marketing_strategy.value', 'marketing_strategy_brand_needs_rel', 'brand_id', 'value_id')
    topics_ids = fields.Many2many('marketing_strategy.brand.topic')
    personality = fields.Selection(PERSONALITY)
    customer_relationship = fields.Selection([('unknown','Unknown'),('friends','Friends'),('colleagues','Colleagues'),('marriage','Marriage'),('partners','Partners'),('parents','Parents'),('lovers','Lovers'),('guru-disciple','Guru-Disciple'),('star-fan','Star-Fan'),('neighbors','Neighbors'),('teammates','Teammates')])
    image_1920 = fields.Image()
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)
    
    
    
class TouchpointTag(models.Model):

    _name = "marketing_strategy.touchpoint.tag"
    _description = "Touchpoint Tag"

    name = fields.Char('Tag Name', required=True, translate=True)
    color = fields.Integer('Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]
    
class Touchpoint(models.Model):
    _name = 'marketing_strategy.touchpoint'
    _description = 'Touchpoint'
    _order = 'name asc'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'image.mixin']
    
    name = fields.Char('Name', required=True)
    active = fields.Boolean(default=True)
    color = fields.Integer('Kanban Color Index')
    sequence = fields.Integer('Sequence')
    state = fields.Selection([
        ('draft', 'Draft'),('testing', 'Testing'),
        ('operating', 'Operating'), ('maintenance', 'Maintenance'), ('cancel', 'Cancelled')],
        string='Status', default='draft', required=True, copy=False, track_visibility='onchange', group_expand='_expand_states')
    ref = fields.Char(string='Internal Reference')
    type = fields.Selection([('online', 'Online'),('offline', 'Offline')], string='Type', required=True, default='online')
    url = fields.Char('URL')
    hub_id = fields.Many2one('res.partner', string='Touchpoints hub', required=True, domain=[('touchpoint_hub','=',True)])
    description = fields.Html('Description')
    tag_ids = fields.Many2many('marketing_strategy.touchpoint.tag', 'marketing_strategy_touchpoint_tags_rel', 'touchpoint_id', 'tag_id', string='Tags')
    story_brand_id = fields.Many2one('marketing_strategy.story_brand')
    plan_id = fields.Many2one('marketing_strategy.plan', string='Marketing Plan')
    buyer_journey_stage = fields.Selection([('awareness','Awareness'),('consideration','Consideration'),('purchase','Purchase'),('service','Service'),('loyalty','Loyalty')], string="Buyer's Journey Stage", default='awareness', required=True, copy=False, track_visibility='onchange', group_expand='_expand_buyer_journey')
    responsible_id = fields.Many2one('res.users', string='Responsible', required=False, default=lambda self: self.env.user)
    image_1920 = fields.Image()
    utm_source_id = fields.Many2one('utm.source')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)  

    def _expand_states(self, states, domain, order):
        return ['draft', 'testing', 'operating', 'maintenance', 'cancel']
        
    def _expand_buyer_journey(self, states, domain, order):
        return ['awareness','consideration','purchase','service', 'loyalty']     
    
class CustomerJob(models.Model):

    _name = "marketing_strategy.value_proposition.customer_job"
    _description = "Customer Job"

    name = fields.Char('Name', required=True, translate=True)
    color = fields.Integer('Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Custumer job name already exists !"),
    ]

class CustomerPain(models.Model):

    _name = "marketing_strategy.value_proposition.customer_pain"
    _description = "Customer Pain"

    name = fields.Char('Name', required=True, translate=True)
    color = fields.Integer('Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Customer pain name already exists !"),
    ]

class CustomerGain(models.Model):

    _name = "marketing_strategy.value_proposition.customer_gain"
    _description = "Customer Gain"

    name = fields.Char('Name', required=True, translate=True)
    color = fields.Integer('Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Custumer gain name already exists !"),
    ]

class PainReliever(models.Model):

    _name = "marketing_strategy.value_proposition.pain_reliever"
    _description = "Pain Reliever"

    name = fields.Char('Name', required=True, translate=True)
    color = fields.Integer('Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Pain reliever name already exists !"),
    ]

class GainCreator(models.Model):

    _name = "marketing_strategy.value_proposition.gain_creator"
    _description = "Gain Creator"

    name = fields.Char('Name', required=True, translate=True)
    color = fields.Integer('Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Gain creator name already exists !"),
    ]

class ValueProposition(models.Model):
    _name = 'marketing_strategy.value_proposition'
    _description = 'Value Propositions'
    _order = 'name asc'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'image.mixin']
    
    def _expand_states(self, states, domain, order):
        return ['draft', 'active', 'done', 'cancel']
    
    name = fields.Char('Name', required=True)   
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('done', 'Completed'),
        ('cancel', 'Cancelled'),
        ],
        string='Status', default='draft', required=True, copy=False, track_visibility='onchange', group_expand='_expand_states')
    color = fields.Integer('Kanban Color Index')
    brand_owner = fields.Many2one('res.partner', required=True)
    description = fields.Html('Description')
    product_type = fields.Selection(PRODUCT_TYPE)
    brand_id = fields.Many2one('marketing_strategy.brand', string='Brand', required=True)
    ref = fields.Char(string='Internal Reference')
    customer_job_ids = fields.Many2many('marketing_strategy.value_proposition.customer_job', 'marketing_strategy_value_propositiont_customer_job_rel', 'value_proposition_id', 'customer_job_id', string='Custumer Jobs')
    customer_pain_ids = fields.Many2many('marketing_strategy.value_proposition.customer_pain', 'marketing_strategy_value_propositiont_customer_pain_rel', 'value_proposition_id', 'customer_pain_id', string='Custumer Pains')
    customer_gain_ids = fields.Many2many('marketing_strategy.value_proposition.customer_gain', 'marketing_strategy_value_propositiont_custumer_gain_rel', 'value_proposition_id', 'custumer_gain_id', string='Custumer Gain')
    pain_reliever_ids = fields.Many2many('marketing_strategy.value_proposition.pain_reliever', 'marketing_strategy_value_propositiont_pain_reliever_rel', 'value_proposition_id', 'pain_reliever_id', string='Pain Reliever')
    gain_creator_ids = fields.Many2many('marketing_strategy.value_proposition.gain_creator', 'marketing_strategy_value_propositiont_gain_creator_rel', 'value_proposition_id', 'gain_creator_id', string='Gain Creator')
    product_l1_id = fields.Many2one('product.product', string='Lebel 1')
    product_l2_id = fields.Many2one('product.product', string='Lebel 2')
    product_l3_id = fields.Many2one('product.product', string='Lebel 3')
    product_l4_id = fields.Many2one('product.product', string='Lebel 4')
    image_1920 = fields.Image()
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)

 
class MeetingPlace(models.Model):

    _name = "marketing_strategy.meeting_place"
    _description = "Meeting place"

    name = fields.Char('Place Name', required=True, translate=True)
    color = fields.Integer('Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Meeting place name already exists !"),
    ]
    
class MeetingContentType(models.Model):

    _name = "marketing_strategy.content_type"
    _description = "Content Type"

    name = fields.Char('Name', required=True, translate=True)
    color = fields.Integer('Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Content type name already exists !"),
    ]
    
class SocialMediaPreference(models.Model):

    _name = "marketing_strategy.social_media_preference"
    _description = "Social Media Preference"

    name = fields.Char('Name', required=True, translate=True)
    color = fields.Integer('Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Social Media name already exists !"),
    ]
    
class BuyerObjection(models.Model):

    _name = "marketing_strategy.buyer_objection"
    _description = "Buyer Objection"

    name = fields.Char('Name', required=True, translate=True)
    color = fields.Integer('Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Objection name already exists !"),
    ]
    
class BuyerGoal(models.Model):

    _name = "marketing_strategy.buyer_goal"
    _description = "Buyer Goal"

    name = fields.Char('Name', required=True, translate=True)
    color = fields.Integer('Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Goal name already exists !"),
    ]
    
class Lifestyle(models.Model):

    _name = "marketing_strategy.buyer_lifestyle"
    _description = "Buyer Lifestyle"

    name = fields.Char('Name', required=True, translate=True)
    color = fields.Integer('Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Buyer lifestyle name already exists !"),
    ]
    
class Competence(models.Model):

    _name = "marketing_strategy.buyer_competence"
    _description = "Buyer Competence"

    name = fields.Char('Name', required=True, translate=True)
    color = fields.Integer('Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Buyer competence name already exists !"),
    ]
    
    
    
   
    
class BuyerPersona(models.Model):
    _name = "marketing_strategy.buyer_persona"
    _description = "Buyer Persona"
    _inherit = ['image.mixin']
    
    @api.model
    def _lang_get(self):
        return self.env['res.lang'].get_installed()
    
    name = fields.Char('Name', required=True, translate=True)
    tribe_id = fields.Many2one('marketing_strategy.tribe', string='Tribe',  required=True)
    color = fields.Integer(string='Color Index', default=0)
    bio = fields.Html('Bio', translate=True)
    age = fields.Integer('Age')
    gender = fields.Selection([('female','Female'),('male','Male'), ('gay','Gay'),('lesbian','Lesbian')], string='Gender')
    status = fields.Selection([('married','Married'),('single','Single'), ('divorced','Divorced'),('widower','Widower')], string='Civil Status')
    children = fields.Integer('# Children')
    income = fields.Monetary('Annual Income', currency_field='company_currency')
    title = fields.Many2one('res.partner.title')
    function = fields.Char(string='Job Position')
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict', domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    zip = fields.Char('Zip')
    city = fields.Char('City')
    lang = fields.Selection(_lang_get, string='Language', default=lambda self: self.env.lang,
                            help="All the emails and documents sent to this contact will be translated in this language.")
    
    competence_ids = fields.Many2many('marketing_strategy.buyer_competence', 'buyer_competence_rel', 'buyer_id', 'competence_id', string='Competences')
    lifestyle_ids = fields.Many2many('marketing_strategy.buyer_lifestyle', 'buyer_buyer_lifestyle_rel', 'buyer_id', 'buyer_lifestyle_id', string='Lifestyle')
    content_type_ids = fields.Many2many('marketing_strategy.content_type', 'buyer_content_rel', 'buyer_id', 'content_type_id', string='Content Type')
    social_media_ids = fields.Many2many('marketing_strategy.social_media_preference', 'buyer_social_media_preferences_rel', 'buyer_id', 'social_media_id', string='Social Media')
    objection_ids = fields.Many2many('marketing_strategy.buyer_objection', 'buyer_objection_rel', 'buyer_id', 'objection_id', string='Objections')
    goal_ids = fields.Many2many('marketing_strategy.buyer_goal', 'buyer_goal_rel', 'buyer_id', 'goal_id', string='Goals')   
    company_currency = fields.Many2one(string='Currency', related='company_id.currency_id', readonly=True, relation="res.currency")
    personality = fields.Selection(PERSONALITY)
    openness = fields.Float(default=50, readonly=True)
    conscientiousness = fields.Float(default=50, readonly=True)
    extraversion = fields.Float(default=50, readonly=True)
    agreeableness = fields.Float(default=50, readonly=True)
    emotional_range = fields.Float(default=50, readonly=True)
    needs_ids = fields.Many2many('marketing_strategy.need', 'marketing_strategy_buyer_persona_needs_rel', 'brand_id', 'need_id')
    values_ids = fields.Many2many('marketing_strategy.value', 'marketing_strategy_buyer_persona_rel', 'brand_id', 'value_id')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)
    

    
class TribeCategory(models.Model):

    _name = "marketing_strategy.tribe.category"
    _description = "Tribe Category"

    name = fields.Char('Name', required=True, translate=True)
   
    
class Tribe(models.Model):
    _name = "marketing_strategy.tribe"
    _description = "Tribe"
    _inherit = ['image.mixin']
    
    name = fields.Char('Tribe Name', required=True, translate=True) 
    category_id = fields.Many2one('marketing_strategy.tribe.category',  string='Category')   
    color = fields.Integer(string='Color Index', default=0)
    meeting_place_ids = fields.Many2many('marketing_strategy.meeting_place', 'tribe_buyer_rel', 'tribe_id', 'meeting_place_id', string='Meeting Places')
    description = fields.Html('Description')
    age_min = fields.Integer('Age Min')
    age_max = fields.Integer('Age Max')
    members_ids = fields.One2many('marketing_strategy.buyer_persona', 'tribe_id', string='Members') 
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)
    


class Plan(models.Model):
    _name = 'marketing_strategy.plan'
    _description = 'Marketing Plan'
    _order = 'name asc'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    
    def _expand_states(self, states, domain, order):
        return ['draft', 'active', 'done', 'cancel']
    
    name = fields.Char('Name', required=True) 
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('done', 'Completed'),
        ('cancel', 'Cancelled'),
        ],
        string='Status', default='draft', required=True, copy=False, track_visibility='onchange', group_expand='_expand_states')
    active = fields.Boolean(default=True,
        help="If the active field is set to False, it will allow you to hide the project without removing it.")
    mission = fields.Html('Description')
    value_proposition_id = fields.Many2one('marketing_strategy.value_proposition', string='Value Proposition', required=True)
    story_brand_id = fields.Many2one('marketing_strategy.story_brand')
    target = fields.Monetary('Target', currency_field='company_currency', track_visibility='always')
    date_start = fields.Date(string='Start Date')
    date_end = fields.Date(string='End Date')
    user_id = fields.Many2one('res.users', string='Responsible', default=lambda self: self.env.user, track_visibility="onchange")
    project_id = fields.Many2one('project.project', string='Project', ondelete='cascade')
    campaigns_ids = fields.One2many('utm.campaign', 'plan_id', string="Campaigns", ondelete='cascade')
    color = fields.Integer(string='Color Index')
    sequence = fields.Integer('Sequence')
    company_currency = fields.Many2one(string='Currency', related='company_id.currency_id', readonly=True, relation="res.currency")
    buyers_persona_ids = fields.Many2many('marketing_strategy.buyer_persona', 'marketing_strategy_plan_buyer_persona_rel', 'plan_id', 'buyer_persona_id', string='Buyers Persona')     
    touchpoints_ids = fields.One2many('marketing_strategy.touchpoint', 'plan_id', string="Touchpoints", ondelete='set null')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)
    

    
    