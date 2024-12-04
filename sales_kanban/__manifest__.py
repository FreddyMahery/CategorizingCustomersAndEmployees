{
    'name': 'Sales Kanban',
    'version': '1.0',
    'summary': 'Kanban View of Sales by Customer',
    'category': 'Sales',
    'author': 'Your Name',
    'depends': ['sale'],  # Dépendance au module "sale"
    'data': [
        'views/sale_order_line_views.xml',
        'views/menus.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}


