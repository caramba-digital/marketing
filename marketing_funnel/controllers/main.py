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

import logging
_logger = logging.getLogger(__name__)

class WebsiteFunnel(http.Controller):

    @http.route([
        '''/touchpoint/<model("funnel.funnel", "[('website_id', 'in', (False, current_website_id))]"):funnel>/page/<model("funnel.page", "[('funnel_id','=',funnel[0])]"):funnel_page>''',
    ], type='http', auth="public", website=True)
    def funnel_page(self, funnel_page=None,  enable_editor=None, **opt):
        page = request.env['funnel.page'].sudo().browse(funnel_page.id)

        values = {
            'page':page,
            'enable_editor': enable_editor,
            }
        response = request.render("marketing_funnel.funnel_page", values)

        request.session[request.session.sid] = request.session.get(request.session.sid, [])
        if not (funnel_page.id in request.session[request.session.sid]):
            request.session[request.session.sid].append(funnel_page.id)
            # Increase counter
            funnel_page.sudo().write({
                'visits': funnel_page.visits + 1,
                'write_date': funnel_page.write_date,
            })
            # Start activities
            if page.activity_ids:
                funnel_page.sudo().process_activities(1)
        return response