# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#


from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    @api.depends('website_id')
    def has_facebook_pixel(self):
        self.has_facebook_pixel = bool(self.facebook_pixel)


    def inverse_has_facebook_pixel(self):
        if not self.has_facebook_pixel:
            self.has_facebook_pixel = False

    facebook_pixel = fields.Char('Facebook Pixel Id', related='website_id.facebook_pixel', readonly=False)
    has_facebook_pixel = fields.Boolean("Facebook Pixel", compute=has_facebook_pixel, inverse=inverse_has_facebook_pixel)
    fb_track_purchase = fields.Boolean('Purchase', related='website_id.fb_track_purchase', readonly=False)
    fb_track_lead = fields.Boolean('Lead', related='website_id.fb_track_lead', readonly=False)
    fb_track_registration = fields.Boolean('Complete Registration', related='website_id.fb_track_registration', readonly=False)
    fb_track_payment_info = fields.Boolean('Add Payment Info', related='website_id.fb_track_payment_info', readonly=False)
    fb_track_add_to_chart = fields.Boolean('Add to Chart', related='website_id.fb_track_add_to_chart', readonly=False)
    fb_track_add_to_wishlist = fields.Boolean('Add to Wishlist', related='website_id.fb_track_add_to_wishlist', readonly=False)
    fb_track_initiate_checkout = fields.Boolean('Initiate Checkout', related='website_id.fb_track_initiate_checkout', readonly=False)
    fb_track_search= fields.Boolean('Search', related='website_id.fb_track_search', readonly=False)
    fb_track_view_content = fields.Boolean('View Content', related='website_id.fb_track_view_content', readonly=False)
    fb_track_contact = fields.Boolean('Contact', related='website_id.fb_track_contact', readonly=False)
    fb_track_customize_product = fields.Boolean('Customize Product', related='website_id.fb_track_customize_product', readonly=False)
    fb_track_donate = fields.Boolean('Donate', related='website_id.fb_track_donate', readonly=False)
    fb_track_find_location = fields.Boolean('Find Location', related='website_id.fb_track_find_location', readonly=False)



