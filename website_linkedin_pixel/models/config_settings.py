# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#


from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    @api.depends('website_id')
    def has_linkedin_pixel(self):
        self.has_linkedin_pixel = bool(self.linkedin_pixel)


    def inverse_has_linkedin_pixel(self):
        if not self.has_linkedin_pixel:
            self.has_linkedin_pixel = False

    linkedin_pixel = fields.Char('Linkedin Pixel Id', related='website_id.linkedin_pixel', readonly=False)
    has_linkedin_pixel = fields.Boolean("Linkedin Pixel", compute=has_linkedin_pixel, inverse=inverse_has_linkedin_pixel)



