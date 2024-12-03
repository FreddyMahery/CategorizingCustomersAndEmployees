{
    'name': 'Gestion des Clients',
    'version': '1.0',
    'summary': 'Afficher les clients dans une vue Kanban',
    'author': 'Freddy',
    'depends': ['base'],  # Module de base d'Odoo
    'data': [
        'views/client_list_view.xml',  # Définition des vues
        'views/client_menu.xml',  # Définition des vues
    ],
    'installable': True,
    'application': True,
     'license': 'LGPL-3',
}
