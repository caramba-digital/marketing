# -*- coding: utf-8 -*-


from odoo import api, fields, models



class Website(models.Model):
    _inherit = 'website'
    
    def _default_social_pinterest(self):
        return self.env.ref('base.main_company').social_pinterest
    
    social_pinterest = fields.Char('Pinterest Account', default=_default_social_pinterest)
    
