# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
 
 
class BrandTag(models.Model):

    _name = "marketing_strategy.brand.tag"
    _description = "Brand Tag"

    name = fields.Char('Tag Name', required=True, translate=True)
    color = fields.Integer('Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]
       
       
class MarketingBrand(models.Model):
    _name = 'marketing_strategy.brand'
    _description = 'Brand'
    _order = 'name asc'

    name = fields.Char('Brand', required=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    tag_ids = fields.Many2many('marketing_strategy.brand.tag', 'marketing_strategy_brand_tags_rel', 'brand_id', 'tag_id', string='Tags') 
    color = fields.Integer('Kanban Color Index')
    image = fields.Binary("Logo", attachment=True,
        help="This field holds the image used as logo for the brand, limited to 1024x1024px.")
    image_medium = fields.Binary("Medium-sized image", attachment=True,
        help="Medium-sized logo of the brand. It is automatically "
             "resized as a 128x128px image, with aspect ratio preserved. "
             "Use this field in form views or some kanban views.")
    image_small = fields.Binary("Small-sized image", attachment=True,
        help="Small-sized logo of the brand. It is automatically "
             "resized as a 64x64px image, with aspect ratio preserved. "
             "Use this field anywhere a small image is required.")
    partner_id = fields.Many2one('res.partner', string='Partner')
    twitter = fields.Char('Twitter Account')
    facebook = fields.Char('Facebook Page')
    linkedin = fields.Char('Linkedin Page')
    youtube = fields.Char('Youtube Channel')
    blog = fields.Char('Blog')
    url = fields.Char('Website')
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            tools.image_resize_images(vals)
        return super(MarketingBrand, self).create(vals_list)


    def write(self, vals):
        tools.image_resize_images(vals)
        return super(MarketingBrand, self).write(vals)
    
    
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
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
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
    image = fields.Binary("Photo", attachment=True,
        help="This field holds the image used as big, limited to 1024x1024px.")
    image_medium = fields.Binary("Medium-sized image", attachment=True,
        help="Medium-sized touchpoint. It is automatically "
             "resized as a 128x128px image, with aspect ratio preserved. "
             "Use this field in form views or some kanban views.")
    image_small = fields.Binary("Small-sized image", attachment=True,
        help="Small-sized touchpoint. It is automatically "
             "resized as a 64x64px image, with aspect ratio preserved. "
             "Use this field anywhere a small image is required.")
    plan_id = fields.Many2one('marketing_strategy.plan', string='Lean Marketing Plan')
    buyer_journey_stage = fields.Selection([('awareness','Awareness'),('consideration','Consideration'),('purchase','Purchase'),('service','Service'),('loyalty','Loyalty')], string="Buyer's Journey Stage", default='awareness', required=True, copy=False, track_visibility='onchange', group_expand='_expand_buyer_journey')
    responsible_id = fields.Many2one('res.users', string='Responsible', required=False, default=lambda self: self.env.user)
    
    def _expand_states(self, states, domain, order):
        return ['draft', 'testing', 'operating', 'maintenance', 'cancel']
        
    def _expand_buyer_journey(self, states, domain, order):
        return ['awareness','consideration','purchase','service', 'loyalty']
        
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            tools.image_resize_images(vals)
        return super(Touchpoint, self).create(vals_list)
    
    
    
    def write(self, vals):
        tools.image_resize_images(vals)
        return super(Touchpoint, self).write(vals)
    
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
    _description = 'Lean Marketing ValuePropositions'
    _order = 'name asc'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char('Name', required=True)
    color = fields.Integer('Kanban Color Index')
    description = fields.Html('Description')
    type = fields.Selection([('product','Product'),('service','Service')], string='Type')
    ref = fields.Char(string='Internal Reference')
    customer_job_ids = fields.Many2many('marketing_strategy.value_proposition.customer_job', 'marketing_strategy_value_propositiont_customer_job_rel', 'value_proposition_id', 'customer_job_id', string='Custumer Jobs')
    customer_pain_ids = fields.Many2many('marketing_strategy.value_proposition.customer_pain', 'marketing_strategy_value_propositiont_customer_pain_rel', 'value_proposition_id', 'customer_pain_id', string='Custumer Pains')
    customer_gain_ids = fields.Many2many('marketing_strategy.value_proposition.customer_gain', 'marketing_strategy_value_propositiont_custumer_gain_rel', 'value_proposition_id', 'custumer_gain_id', string='Custumer Gain')
    pain_reliever_ids = fields.Many2many('marketing_strategy.value_proposition.pain_reliever', 'marketing_strategy_value_propositiont_pain_reliever_rel', 'value_proposition_id', 'pain_reliever_id', string='Pain Reliever')
    gain_creator_ids = fields.Many2many('marketing_strategy.value_proposition.gain_creator', 'marketing_strategy_value_propositiont_gain_creator_rel', 'value_proposition_id', 'gain_creator_id', string='Gain Creator')
    products_ids = fields.Many2many('product.product',  'marketing_strategy_value_propositiont_product_rel', 'value_proposition_id', 'product_id', string='Products or Services')
    
    image = fields.Binary("Photo", attachment=True,
        help="This field holds the image used as big, limited to 1024x1024px.")
    image_medium = fields.Binary("Medium-sized image", attachment=True,
        help="Medium-sized touchpoint. It is automatically "
             "resized as a 128x128px image, with aspect ratio preserved. "
             "Use this field in form views or some kanban views.")
    image_small = fields.Binary("Small-sized image", attachment=True,
        help="Small-sized touchpoint. It is automatically "
             "resized as a 64x64px image, with aspect ratio preserved. "
             "Use this field anywhere a small image is required.")
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            tools.image_resize_images(vals)
        return super(ValueProposition, self).create(vals_list)
    
    
    
    def write(self, vals):
        tools.image_resize_images(vals)
        return super(ValueProposition, self).write(vals)
    

 
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
    
class Preference(models.Model):

    _name = "marketing_strategy.buyer_preference"
    _description = "Buyer Preference"

    name = fields.Char('Name', required=True, translate=True)
    color = fields.Integer('Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Buyer preference name already exists !"),
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
    
    @api.model
    def _lang_get(self):
        return self.env['res.lang'].get_installed()
    
    name = fields.Char('Place Name', required=True, translate=True)
    tribe_id = fields.Many2one('marketing_strategy.tribe', string='Tribe',  required=True)
    color = fields.Integer(string='Color Index', default=0)
    bio = fields.Html('Bio', translate=True)
    age_min = fields.Integer('Age Min')
    age_max = fields.Integer('Age Max')
    gender = fields.Selection([('female','Female'),('male','Male'), ('gay','Gay'),('lesbian','Lesbian')], string='Gender')
    status = fields.Selection([('married','Married'),('single','Single'), ('divorced','Divorced'),('widower','Widower')])
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
    
    image = fields.Binary("Image", attachment=True,
        help="This field holds the image used as avatar for this contact, limited to 1024x1024px",)
    image_medium = fields.Binary("Medium-sized image", attachment=True,
        help="Medium-sized image of this contact. It is automatically "\
             "resized as a 128x128px image, with aspect ratio preserved. "\
             "Use this field in form views or some kanban views.")
    image_small = fields.Binary("Small-sized image", attachment=True,
        help="Small-sized image of this contact. It is automatically "\
             "resized as a 64x64px image, with aspect ratio preserved. "\
             "Use this field anywhere a small image is required.")
    competence_ids = fields.Many2many('marketing_strategy.buyer_competence', 'buyer_competence_rel', 'buyer_id', 'competence_id', string='Competences')
    preference_ids = fields.Many2many('marketing_strategy.buyer_preference', 'buyer_preference_rel', 'buyer_id', 'cpreference_id', string='Preferences')
    content_type_ids = fields.Many2many('marketing_strategy.content_type', 'buyer_content_rel', 'buyer_id', 'content_type_id', string='Content Type Preferences')
    social_media_ids = fields.Many2many('marketing_strategy.social_media_preference', 'buyer_social_media_preferences_rel', 'buyer_id', 'social_media_id', string='Social Media Preferences')
    objection_ids = fields.Many2many('marketing_strategy.buyer_objection', 'buyer_objection_rel', 'buyer_id', 'objection_id', string='Objections')
    goal_ids = fields.Many2many('marketing_strategy.buyer_goal', 'buyer_goal_rel', 'buyer_id', 'goal_id', string='Goals')    
    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.user.company_id.id)
    company_currency = fields.Many2one(string='Currency', related='company_id.currency_id', readonly=True, relation="res.currency")
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            tools.image_resize_images(vals)
        return super(BuyerPersona, self).create(vals_list)

    def write(self, vals):
        tools.image_resize_images(vals)
        return super(BuyerPersona, self).write(vals)
    

    
class TribeCategory(models.Model):

    _name = "marketing_strategy.tribe.category"
    _description = "Tribe Category"

    name = fields.Char('Name', required=True, translate=True)
   
    
class Tribe(models.Model):
    _name = "marketing_strategy.tribe"
    _description = "Tribe"
    
    name = fields.Char('Tribe Name', required=True, translate=True) 
    category_id = fields.Many2one('marketing_strategy.tribe.category',  string='Category')   
    color = fields.Integer(string='Color Index', default=0)
    meeting_place_ids = fields.Many2many('marketing_strategy.meeting_place', 'tribe_buyer_rel', 'tribe_id', 'meeting_place_id', string='Meeting Places')
    description = fields.Html('Description')
    members_ids = fields.One2many('marketing_strategy.buyer_persona', 'tribe_id', string='Members') 
   

class ConsumerTrend(models.Model):
    _name = "marketing_strategy.consumer_trend"
    _description = "Consumer Trend Canvas"
    
    def _expand_states(self, states, domain, order):
        return ['draft', 'active', 'done', 'cancel']
    
    name = fields.Char('Area Name', required=True, index=True)    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('done', 'Completed'),
        ('cancel', 'Cancelled'),
        ],
        string='Status', default='draft', required=True, copy=False, track_visibility='onchange', group_expand='_expand_states')
    internal_factor_ids = fields.One2many('marketing_strategy.internal_factor_question', 'consumer_trend_id', string='Internal Factors')
    external_factor_ids = fields.One2many('marketing_strategy.external_factor_question', 'consumer_trend_id', string='External Factors')
    
class KeyResource(models.Model):

    _name = "marketing_strategy.key_resources"
    _description = "Key Resource"

    name = fields.Char('Tag Name', required=True, translate=True)
    color = fields.Integer('Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]
    
class KeyResourceFinancial(models.Model):

    _name = "marketing_strategy.key_resources_financial"
    _description = "Key Financial Resource"

    name = fields.Char('Tag Name', required=True, translate=True)
    color = fields.Integer('Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]
    
class KeyResourceIntellectual(models.Model):

    _name = "marketing_strategy.key_resources_intellectual"
    _description = "Key Intellectual Resource"

    name = fields.Char('Tag Name', required=True, translate=True)
    color = fields.Integer('Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]
    
class CustomerRelationships(models.Model):

    _name = "marketing_strategy.custumer_relationship"
    _description = "Key Intellectual Resource"

    name = fields.Char('Tag Name', required=True, translate=True)
    color = fields.Integer('Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]
    
    
class CustomerChannels(models.Model):

    _name = "marketing_strategy.channels"
    _description = "Channels"

    name = fields.Char('Tag Name', required=True, translate=True)
    color = fields.Integer('Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]
    

class KeyPhysicalResource(models.Model):

    _name = "marketing_strategy.key_physical_resource"
    _description = "Key Physical Resource"

    name = fields.Char('Tag Name', required=True, translate=True)
    color = fields.Integer('Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]    
    

class Plan(models.Model):
    _name = 'marketing_strategy.plan'
    _description = 'Lean Marketing Plan'
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
    value_proposition_id = fields.Many2one('marketing_strategy.value_proposition', string='ValueProposition', required=True)
    target = fields.Monetary('Target', currency_field='company_currency', track_visibility='always')
    date_start = fields.Date(string='Start Date')
    date_end = fields.Date(string='End Date')
    user_id = fields.Many2one('res.users', string='Product owner', default=lambda self: self.env.user, track_visibility="onchange")
    project_id = fields.Many2one('project.project', string='Project', ondelete='cascade')
    campaigns_ids = fields.One2many('utm.campaign', 'plan_id', string="Campaigns", ondelete='cascade')
    color = fields.Integer(string='Color Index')
    sequence = fields.Integer('Sequence')
    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.user.company_id.id)
    company_currency = fields.Many2one(string='Currency', related='company_id.currency_id', readonly=True, relation="res.currency")
    buyers_persona_ids = fields.Many2many('marketing_strategy.buyer_persona', 'marketing_strategy_plan_buyer_persona_rel', 'plan_id', 'buyer_persona_id', string='Buyers Persona')     
    key_partners_ids = fields.Many2many('res.partner', 'marketing_strategy_plan_res_partner_rel','plan_id', 'res_partner_id', string='Key Partners') 
    key_activities_ids = fields.Many2many('project.task', 'marketing_strategy_plan_project_task_rel', 'plan_id', 'task_id', string='Key Activities')
    key_human_resources_ids = fields.Many2many('res.partner', 'marketing_strategy_plan_hr_res_partner_rel','plan_id', 'res_partner_id', string='Human Resources') 
    key_physical_resource_ids = fields.Many2many('product.product', 'marketing_strategy_plan_product_rel','plan_id', 'product_id', string='Physical Resources') 
    key_physical_resource_tag_ids = fields.Many2many('marketing_strategy.key_physical_resource', 'marketing_strategy_plan_key_physical_resource_rel','plan_id', 'tag_id', string='Physical Resources') 
    key_resources_ids = fields.Many2many('marketing_strategy.key_resources', 'marketing_strategy_key_resources_rel', 'plan_id', 'tag_id', string='Tags')
    key_resources_financial_ids = fields.Many2many('marketing_strategy.key_resources_financial', 'marketing_strategy_key_resources_financial_rel', 'plan_id', 'tag_id', string='Tags')
    key_resources_intellectual_ids = fields.Many2many('marketing_strategy.key_resources_intellectual', 'marketing_strategy_key_resources_intellectual_rel', 'plan_id', 'tag_id', string='Tags')
    value_propositions = fields.Many2many(related='value_proposition_id.gain_creator_ids')
    relationship_ids = fields.Many2many('marketing_strategy.custumer_relationship', 'marketing_strategy_plan_custumer_relationship_rel', 'plan_id', 'relationship_id', string='Tags')
    channel_ids = fields.Many2many('marketing_strategy.channels', 'marketing_strategy_plan_channel_rel', 'plan_id', 'channel_id', string='Tags')
    cost_structure_ids = fields.Many2many('account.account', 'marketing_strategy_plan_cost_structure_rel', 'plan_id', 'account_id', string="Cost Structure")
    revenue_streams_ids = fields.Many2many('account.account','marketing_strategy_revenue_stream_rel', 'plan_id', 'account_id', string="Revenue Streams")   
    touchpoints_ids = fields.One2many('marketing_strategy.touchpoint', 'plan_id', string="Touchpoints", ondelete='set null')

    

    
    
