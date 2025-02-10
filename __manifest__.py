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
    'depends': ['base','mail','purchase'],

    # always loaded
    'data': [
        'security/supplier_management_security.xml',
        'security/ir.model.access.csv',
        'security/record_rule.xml',
        'views/portal_rfp_templates.xml',
        'views/email_template.xml',
        'views/ir_sequence.xml',
        'views/views.xml',
        'views/rfp_views.xml',
        'views/supplier_registration_view.xml',
        'views/templates.xml',
        'data/otp_email_template.xml',
        'wizard/reject_reason_wizard.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

