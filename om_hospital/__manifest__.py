# -*- coding: utf-8 -*-
{
    'name': "Hospital Management",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Youssef",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'sale', 'board', 'web', 'web_widget_model_viewer', 'web_domain_field'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'wizards/create_appointment.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/patient.xml',
        'views/appointment.xml',
        'views/doctor.xml',
        'views/lab.xml',
        'views/settings.xml',
        'views/dashboard.xml',
        'views/server_action.xml',
        'views/website_form.xml',
        'views/inherit_sale_order.xml',
        'data/sequence.xml',
        'data/mail_template.xml',
        'data/cron.xml',
        'reports/patient_card.xml',
        'reports/report.xml',
        'reports/sale_report_inherit.xml',
        'reports/appointment.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
