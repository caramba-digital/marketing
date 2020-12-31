odoo.define('marketing_funnels.funnels', function (require) {
    'use strict';

    var core = require('web.core');
    var wUtils = require('website.utils');
    var publicWidget = require('web.public.widget');
    var qweb = core.qweb;
    var _t = core._t;
    
  
    
    publicWidget.registry.js_get_social_proof = publicWidget.Widget.extend({
        selector: '.social-proof-container',
        disabledInEditableMode: false,
        start: function () {
            let toastHeader= ''
            let body = '<div class="media"><img src="/web/static/src/img/favicon.ico" class="mr-3"/> <div class="media-body"> <h5 class="mt-0">Media heading</h5>Cras sit amet nibh libero, in gravida nulla. Nulla vel metus scelerisque ante sollicitudin. Cras purus odio, vestibulum in vulputate at, tempus viverra turpis. Fusce condimentum nunc ac nisi vulputate fringilla. Donec lacinia congue felis in faucibus.</div></div>'
            this.do_notify(_t("Success"), _t("Your signature request has been sent."))

        },


        
    });
    
})