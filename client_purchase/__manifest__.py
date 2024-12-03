{
    'name': 'Client Purchase Module',
    'version': '1.0',
    'depends': ['base', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/client_purchase_menu.xml',
        'views/res_partner_inherit_views.xml',
        'views/purchase_report_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
