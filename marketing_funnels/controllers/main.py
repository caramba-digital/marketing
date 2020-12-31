# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#

import json
import werkzeug
import itertools
import pytz
import babel.dates
from collections import OrderedDict

from odoo import http, fields
from odoo.addons.http_routing.models.ir_http import slug, unslug
from odoo.addons.website.controllers.main import QueryURL
from odoo.http import request
from odoo.osv import expression
from odoo.tools import html2plaintext
from odoo.tools.misc import get_lang

from odoo.addons.website_form.controllers.main import WebsiteForm

import logging
_logger = logging.getLogger(__name__)

class WebsiteFunnel(http.Controller):

    def _get_pricelist_context(self):
        pricelist_context = dict(request.env.context)
        pricelist = False
        if not pricelist_context.get('pricelist'):
            pricelist = request.website.get_current_pricelist()
            pricelist_context['pricelist'] = pricelist.id
        else:
            pricelist = request.env['product.pricelist'].browse(pricelist_context['pricelist'])

        return pricelist_context, pricelist


    @http.route([
        '''/touchpoint/<model("funnel.funnel", "[('website_id', 'in', (False, current_website_id))]"):funnel>/page/<model("funnel.page", "[('funnel_id','=',funnel[0])]"):funnel_page>''',
    ], type='http', auth="public", website=True)
    def funnel_page(self, funnel_page=None,  enable_editor=None, **opt):
        page = request.env['funnel.page'].sudo().browse(funnel_page.id)
        values = {
            'page':page,
            'enable_editor': enable_editor,
            'main_object': funnel_page
            }
        resource = page.type_id.resource
        if resource=='product':
            values.update(self._prepare_product_values(page.product_id))
        elif  resource=='offer':
            set=2
        elif  resource=='catalog':
            values['products']= page.products_ids
        elif  resource=='random':
            set=2
        elif  resource=='event':  
            values['event']= page.event_id
        elif  resource=='newsletter':  
            set=2
        elif  resource=='lead':  
            set=2
        elif  resource=='coupon_program': 
            set=2 
        elif  resource=='badge':  
            set=2
        else:  
            set=2  
        response = request.render("marketing_funnels.funnel_page", values)
        request.session[request.session.sid] = request.session.get(request.session.sid, [])
        if not (funnel_page.id in request.session[request.session.sid]):
            request.session[request.session.sid].append(funnel_page.id)
            # Increase counter
            funnel_page.sudo().write({
                'visits': funnel_page.visits + 1,
                'write_date': funnel_page.write_date,
            })
            # Start activities
        return response



    def _prepare_product_values(self, product, **kwargs):
        add_qty = int(kwargs.get('add_qty', 1))
        product_context = dict(request.env.context, quantity=add_qty,
                                active_id=product.id,
                                partner=request.env.user.partner_id)
        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
        attrib_set = {v[1] for v in attrib_values}
        pricelist = request.website.get_current_pricelist()
        if not product_context.get('pricelist'):
                product_context['pricelist'] = pricelist.id
                product = product.with_context(product_context)

            # Needed to trigger the recently viewed product rpc
        view_track = request.website.viewref("website_sale.product").track
        return {
                'pricelist': pricelist,
                'attrib_values': attrib_values,
                'attrib_set': attrib_set,
                'main_object': product,
                'product': product,
                'add_qty': add_qty,
                'view_track': view_track,
            }
    @http.route(['/funnel/get_social_proof'], type='json', auth='public', website=True)
    def get_social_proof(self, template, **kwargs):
        return request.website.viewref(template)._render({})
        







class WebsiteForm(WebsiteForm):
    
    # Check and insert values from the form on the model <model> + validation phone fields
    @http.route('/funnel_form/<string:model_name>', type='http', auth="public", methods=['POST'], website=True)
    def website_form(self, model_name, **kwargs):
        model_record = request.env['ir.model'].sudo().search([('model', '=', model_name), ('website_form_access', '=', True)])
        if model_record and hasattr(request.env[model_name], 'phone_format'):
            try:
                data = self.extract_data(model_record, request.params)
            except:
                # no specific management, super will do it
                pass
            else:
                record = data.get('record', {})
                phone_fields = self._get_phone_fields_to_validate()
                country = request.env['res.country'].browse(record.get('country_id'))
                contact_country = country.exists() and country or self._get_country()
                for phone_field in phone_fields:
                    if not record.get(phone_field):
                        continue
                    number = record[phone_field]
                    fmt_number = request.env[model_name].phone_format(number, contact_country)
                    request.params.update({phone_field: fmt_number})

        if model_name == 'crm.lead' and not request.params.get('state_id'):
            geoip_country_code = request.session.get('geoip', {}).get('country_code')
            geoip_state_code = request.session.get('geoip', {}).get('region')
            if geoip_country_code and geoip_state_code:
                state = request.env['res.country.state'].search([('code', '=', geoip_state_code), ('country_id.code', '=', geoip_country_code)])
                if state:
                    request.params['state_id'] = state.id
        return super(WebsiteForm, self).website_form(model_name, **kwargs)
        


    
    

    