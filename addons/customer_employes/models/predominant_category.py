from odoo import models, fields, api

class EmployeePredominantCategory(models.Model):
    _inherit = 'hr.employee'  # On hérite du modèle `hr.employee`

    # Champ pour afficher la catégorie prédominante
    predominant_category = fields.Char(string="Predominant Category", compute='_compute_predominant_category')

    # Champ relationnel pour lier les commandes de vente à l'employé
    sale_order_ids = fields.One2many('sale.order', 'user_id', string="Sales Orders")  # Relation One2many avec sale.order via user_id

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)  # Ajout du champ company_id


    @api.depends('sale_order_ids')
    def _compute_predominant_category(self):
        for employee in self:
            # Dictionnaire pour compter les quantités des catégories de produits traitées par l'employé
            category_count = {}

            # Parcours des commandes de l'employé
            for order in employee.sale_order_ids:
                for line in order.order_line:
                    # Récupérer la catégorie de produit
                    product_category = line.product_id.categ_id.name
                    if product_category not in category_count:
                        category_count[product_category] = 0
                    category_count[product_category] += line.product_uom_qty

            # Déterminer la catégorie prédominante (celle avec la quantité la plus élevée)
            if category_count:
                predominant_category = max(category_count, key=category_count.get)
                employee.predominant_category = predominant_category
            else:
                employee.predominant_category = 'Aucune catégorie'

