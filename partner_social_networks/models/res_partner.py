# -*- coding: utf-8 -*-
# LICENSE GNU GENERAL PUBLIC LICENSE Version 3

from odoo import models, fields, api


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    facebook_profile = fields.Char()
    twitter_profile = fields.Char()
    instagram_profile = fields.Char()
    linkedin_profile = fields.Char()
    tiktok_profile = fields.Char()
    pinterest_profile = fields.Char()
    youtube_channel = fields.Char()
    github_profile = fields.Char()
    blog = fields.Char()
    blog_2 = fields.Char()
    facebook_page = fields.Char()
    linkedin_page = fields.Char()
    google_my_business = fields.Char()
    whatsapp_businnes = fields.Char()
    messenger = fields.Char()
    telegram = fields.Char() 


    