# -*- coding: utf-8 -*-
# LICENSE GNU GENERAL PUBLIC LICENSE Version 3


from odoo.addons.http_routing.models.ir_http import slugify
from odoo.addons.http_routing.models.ir_http import slug
from odoo.tools.translate import html_translate
from odoo import api, fields, models

class Funnel(models.Model):
    _name = 'funnel.funnel'
    _description = 'Funnels'
    _inherit = ['mail.thread', 'website.seo.metadata', 'website.multi.mixin']
    _order = 'name'
    
    name = fields.Char('Funnel Name', required=True, translate=True)
    subtitle = fields.Char('Funnel Subtitle', translate=True)
    active = fields.Boolean('Active', default=True)
    description = fields.Text(string='Description')
    user_id = fields.Many2one('res.users', string='Responsible', index=True, tracking=True, default=lambda self: self.env.user)
    
class FunnelPage(models.Model):
    _name = 'funnel.page'
    _inherit = ['mail.thread', 'website.seo.metadata', 'website.published.multi.mixin']
    _order = 'name'
    
    def _compute_website_url(self):
        super(FunnelPage, self)._compute_website_url()
        for page in self:
            page.website_url = "/funnel/page/%s" % slug(page)
            
    def _default_content(self):
        return '''
            <div class="swiper-container">
                <div class="swiper-wrapper">
                  <div class="swiper-slide">Slide 1</div>
                  <div class="swiper-slide">Slide 2</div>
                  <div class="swiper-slide">Slide 3</div>
                  <div class="swiper-slide">Slide 4</div>
                  <div class="swiper-slide">Slide 5</div>
                </div>
                <div class="swiper-pagination"></div>
              </div>
        '''
            
    #url = fields.Char('Page URL')
    name = fields.Char(' Name', required=True, translate=True)
    color = fields.Integer(string='Color Index')    
    sequence = fields.Integer('Sequence')
    funnel_id =  fields.Many2one('funnel.funnel', string='Parent Page', index=True, ondelete='cascade')
    parent_id = fields.Many2one('funnel.page', string='Parent Page', index=True, ondelete='cascade')
    child_ids = fields.One2many('funnel.page', 'parent_id', string='Child Page')
    content = fields.Html('Content', default=_default_content, translate=html_translate, sanitize=False)
    create_date = fields.Datetime('Created on', index=True, readonly=True)
    published_date = fields.Datetime('Published Date')
    post_date = fields.Datetime('Publishing date', compute='_compute_post_date', inverse='_set_post_date', store=True,
                                help="The blog post will be visible for your visitors as of this date on the website if it is set as published.")
    create_uid = fields.Many2one('res.users', 'Created by', index=True, readonly=True)
    write_date = fields.Datetime('Last Updated on', index=True, readonly=True)
    write_uid = fields.Many2one('res.users', 'Last Contributor', index=True, readonly=True)
    visits = fields.Integer('No of Views', copy=False)
    website_id = fields.Many2one(related='funnel_id.website_id', readonly=True)
 
