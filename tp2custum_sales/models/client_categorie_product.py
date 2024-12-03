from odoo import models, fields

class ResPartner(models.Model):
    _inherit = "res.partner"

    predominant_category = fields.Char(string="Catégorie Prédominante")
    
    def update_category(self):
        for partner in self:
            # Logique pour calculer la catégorie prédominante basée sur l'historique des achats
            # Exemple : Compter les produits achetés dans chaque catégorie et déterminer la prédominante
            category_count = {}
            orders = self.env['sale.order'].search([('partner_id', '=', partner.id)])
            for order in orders:
                for line in order.order_line:
                    category = line.product_id.categ_id.name
                    category_count[category] = category_count.get(category, 0) + 1
            
            # Déterminer la catégorie prédominante basée sur le seuil
            threshold = 10  # Seuil d'exemple
            predominant = max(category_count, key=category_count.get) if category_count else None
            
            if category_count.get(predominant, 0) >= threshold:
                partner.predominant_category = predominant
            else:
                partner.predominant_category = None