# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#


from odoo import api, fields, models, _


class Website(models.Model):
    _inherit = 'website'


    facebook_pixel = fields.Char('Facebook Pixel Id')
    fb_track_purchase = fields.Boolean('Purchase', default=False)
    fb_track_lead = fields.Boolean('Lead', default=False)
    fb_track_registration = fields.Boolean('Complete Registration', default=False)
    fb_track_payment_info = fields.Boolean('Add Payment Info', default=False)
    fb_track_add_to_chart = fields.Boolean('Add to Chart', default=False)
    fb_track_add_to_wishlist = fields.Boolean('Add to Wishlist', default=False)
    fb_track_initiate_checkout = fields.Boolean('Initiate Checkout', default=False)
    fb_track_search= fields.Boolean('Search', default=False)
    fb_track_view_content = fields.Boolean('View Content', default=False)
    fb_track_contact = fields.Boolean('Contact', default=False)
    fb_track_customize_product = fields.Boolean('Customize Product', default=False)
    fb_track_donate = fields.Boolean('Donate', default=False)
    fb_track_find_location = fields.Boolean('Find Location', default=False)
    
