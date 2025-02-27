# -*- coding: utf-8 -*-
{
    'name': "supplier_management",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "Anowarul Karim",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['purchase','website'],

    # always loaded
    'data': [
        'security/supplier_management_security.xml',
        'security/ir.model.access.csv',
        'data/supplier_registration_demo.xml',
        'data/RFP_demo.xml',
        'data/product_line_demo.xml',
        'data/RFQ_demo.xml',
        'views/supplier_res_web.xml',
        'views/portal_rfp_templates.xml',
        'views/portal_rfq.xml',
        'views/email_template.xml',
        'views/purchase_order_line_inherit.xml',
        'views/bank_views_extended.xml',
        'views/res_partner_extended.xml',
        'views/res_partner_inherit_views.xml',
        'wizard/rfp_report.xml',
        'views/supplier_rfp_report.xml',
        'views/ir_sequence.xml',
        'views/views.xml',
        'views/rfp_views.xml',
        'views/supplier_registration_view.xml',
        'views/templates.xml',
        'views/menus.xml',
        'data/otp_email_template.xml',
        'wizard/reject_reason_wizard.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'assets':{
        'web.assets_backend':{
            'supplier_management/static/src/components/**/*.js',
            'supplier_management/static/src/components/**/*.xml',
            'supplier_management/static/src/components/**/*.css',
        }
    }
}

