# -*- coding: utf-8 -*-
{
    'name': "Customer Employes",

    'summary': "This is a modul for our TP2",

    'description': """
Long description of module's purpose
    """,

    'license': 'OPL-1',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'application': True,
    'installable': True,

    # any module necessary for this one to work correctly
    'depends': ['base','sale','hr'],

    # always loaded
    'data': [
         'security/ir.model.access.csv',
        #  'views/predominant_category_menus.xml',
         'views/client_category_views.xml',
         'views/client_views.xml',
         'views/predominant_category_views.xml',
         'views/sale_report_view.xml',
         'views/menu.xml'
    #     'views/views.xml',
    #     'views/templates.xml',
     ]
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}

