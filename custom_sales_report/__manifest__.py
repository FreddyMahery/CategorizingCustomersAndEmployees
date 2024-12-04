{
    'name': 'Custom Sales Report',
    'version': '1.0',
    'author': 'Freddy',
    'category': 'Sales',
    'summary': 'Affiche les noms des clients avec leurs achats',
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_report_inherit_views.xml',
        'views/category_config_views.xml',
        'views/sale_report_menu.xml',

    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
