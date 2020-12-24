odoo.define('marketing_funnels.funnels', function (require) {
    'use strict';
    
    var wUtils = require('website.utils');
    var publicWidget = require('web.public.widget');
    
  
    
    publicWidget.registry.js_get_social_proof = publicWidget.Widget.extend({
        selector: '.social-proof-container',
        disabledInEditableMode: false,

        willStart: function () {
        },

        start: function () {
        },

        destroy: function () {
        },
        
    });
    
})