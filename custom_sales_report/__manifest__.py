{
    'name': 'Custom Sales Report',
    'version': '1.0',
    'author': 'Freddy',
    'category': 'Sales',
    'summary': 'Affiche les noms des clients avec leurs achats',
    'depends': ['sale'],
    'data': [
        'views/sale_report_inherit_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
