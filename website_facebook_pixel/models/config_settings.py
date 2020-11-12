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



