# __manifest__.py

{
    'name': 'Custom Sales',
    'version': '1.0',
    'summary': 'Module personnalisé pour gérer la récupération des produits et des clients.',
    'description': """
        Ce module ajoute des fonctionnalités personnalisées pour récupérer
        et gérer la liste des produits et des clients.
    """,
    'website': 'http://www.tonsite.com',
    'category': 'Sales',
    'depends': ['base', 'sale'],  # Dépendances nécessaires pour utiliser les modèles natifs
    'data': [
        'security/ir.model.access.csv',
        'views/custom_sales_views.xml',
        'views/custom_sales_menus.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
