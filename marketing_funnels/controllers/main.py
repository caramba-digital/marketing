# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#

import json
import werkzeug
import itertools
import pytz
import babel.dates
from collections import OrderedDict
import string
import random
from datetime import datetime

from odoo import http, fields, _
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
        if resource=='product' or resource=='offer':
            values.update(self._prepare_product_values(page.product_id))
        elif  resource=='catalog':
            values['products']= page.products_ids
        elif  resource=='random':
            set=2
        elif  resource=='event':  
            values['event']= page.event_id
        elif  resource=='newsletter':  
            if page.button_position=='left':
                values['align']='text-left s_website_form_no_submit_label'
            elif page.button_position=='center':
                values['align']='text-center s_website_form_no_submit_label'
            elif page.button_position=='right':
                values['align']='text-right s_website_form_no_submit_label'
            else:
                values['align']=' '
        elif  resource=='lead':  
            if page.button_position=='left':
                values['align']='text-left s_website_form_no_submit_label'
            elif page.button_position=='center':
                values['align']='text-center s_website_form_no_submit_label'
            elif page.button_position=='right':
                values['align']='text-right s_website_form_no_submit_label'
            else:
                values['align']=' '
            values['call_to_action'] =  {'suscribe':_('Subscribe'),'apply':_('Apply'),'reserve':_('Reserve'),'download':_('Download'),'get_offer':_('Get Offer'),'quote':_('Quote'),'sign_up':_('Sign Up'),'more_info':_('More Information')}
            values['required_ids']= {'name':self._id_generator(),'phone':self._id_generator(),'email':self._id_generator(),'company':self._id_generator(), 'question':self._id_generator(),'subject':self._id_generator}
        elif  resource=='coupon_program': 
            set=2 
        elif  resource=='badge':  
            set=2
        else:  
            set=2  
        response = request.render("marketing_funnels.funnel_page", values)
        if page.is_published:
            page.visits +=1
            page.last_date = datetime.now()
            visitor = request.env['website.visitor']._get_visitor_from_request()
            if page.activity_ids:
                funnel_page.sudo().process_activities(visitor.id)
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

    def _id_generator(self, size=11, chars=string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
        








        


    
    

    