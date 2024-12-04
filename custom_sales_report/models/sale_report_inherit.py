from odoo import models, fields, api
from collections import defaultdict

class CustomSaleReport(models.Model):
    _inherit = 'sale.report'

    customer_purchases = fields.Text(
        string="Achats du client",
        compute="_compute_customer_purchases",
        store=False
    )

    customer_purchase_quantity = fields.Text(
    string="Quantité totale",
    compute="_compute_customer_purchases",
    store=False
    )

    # @api.depends('partner_id', 'product_id', 'product_uom_qty')
    # def _compute_customer_purchases(self):
    #     """ Regroupe les achats du client en texte formaté """
    #     for report in self:
    #         purchases = self.env['sale.report'].search([
    #             ('partner_id', '=', report.partner_id.id)
    #         ])
    #         report.customer_purchases = "\n".join(
    #             f"{purchase.product_id.display_name} - {purchase.product_uom_qty}" 
    #             for purchase in purchases
    #         )

    # @api.depends('partner_id', 'product_id', 'product_uom_qty')
    # def _compute_customer_purchases(self):
    #     """ Regroupe les achats par client et additionne les quantités des produits identiques """
    #     for report in self:
    #         # Regroupe les produits similaires avec leurs quantités pour ce client
    #         purchases = self.env['sale.report'].search([
    #             ('partner_id', '=', report.partner_id.id)
    #         ])
            
    #         product_quantities = defaultdict(float)  # Pour regrouper les quantités par produit
    #         for purchase in purchases:
    #             if purchase.product_id:
    #                 product_quantities[purchase.product_id.display_name] += purchase.product_uom_qty

    #         # Formater les achats sous forme de texte
    #         report.customer_purchases = "\n".join(
    #             f"{product_name} - {quantity}" 
    #             for product_name, quantity in product_quantities.items()
    #         )
    # @api.depends('partner_id', 'product_id', 'product_uom_qty')
    # def _compute_customer_purchases(self):
    #     """ Regroupe les achats pour chaque client et élimine les duplications """
    #     # Récupérer tous les enregistrements nécessaires
    #     grouped_purchases = defaultdict(lambda: defaultdict(float))
    #     for record in self.env['sale.report'].search([]):
    #         if record.partner_id and record.product_id:
    #             grouped_purchases[record.partner_id][record.product_id.display_name] += record.product_uom_qty

    #     # Mettre à jour chaque record unique avec ses données regroupées
    #     for report in self:
    #         if report.partner_id:
    #             purchases = grouped_purchases.get(report.partner_id, {})
    #             report.customer_purchases = "\n".join(
    #                 f"{product_name} - {quantity}"
    #                 for product_name, quantity in purchases.items()
    #             )
    #         else:
    #             report.customer_purchases = ""
    # @api.depends('partner_id', 'product_id', 'product_uom_qty')
    # def _compute_customer_purchases(self):
    #     """ Regroupe les achats des clients et additionne les quantités des produits identiques,
    #     tout en évitant les doublons d'affichage """
    #     # Regrouper les achats par client et produit
    #     customer_purchases = defaultdict(lambda: defaultdict(float))
    #     displayed_customers = set()  # Ensemble pour garder une trace des clients déjà affichés

    #     # Parcours de tous les enregistrements de ventes
    #     for record in self.env['sale.report'].search([]):
    #         if record.partner_id and record.product_id:
    #             customer_purchases[record.partner_id][record.product_id.display_name] += record.product_uom_qty

    #     # Mettre à jour les enregistrements avec la liste d'achats combinée
    #     for report in self:
    #         if report.partner_id:
    #             # Vérifier si le client a déjà été traité
    #             if report.partner_id in displayed_customers:
    #                 # Si déjà affiché, on ne montre rien
    #                 report.customer_purchases = ""
    #             else:
    #                 # Ajouter le client à l'ensemble des clients affichés
    #                 displayed_customers.add(report.partner_id)

    #                 # Récupérer les achats du client spécifique et les combiner
    #                 purchases = customer_purchases.get(report.partner_id, {})
    #                 # Création d'une chaîne avec les produits et leurs quantités
    #                 report.customer_purchases = "\n".join(
    #                     f"{product_name} - {quantity}"
    #                     for product_name, quantity in purchases.items()
    #                 )
    #         else:
    #             report.customer_purchases = ""
    # @api.depends('partner_id', 'product_id', 'product_uom_qty')
    # def _compute_customer_purchases(self):
    #     """Regroupe les achats des clients et affiche les produits et quantités dans des champs distincts."""
    #     # Regrouper les achats par client et produit
    #     customer_purchases = defaultdict(lambda: defaultdict(float))
    #     for record in self.env['sale.report'].search([]):
    #         if record.partner_id and record.product_id:
    #             customer_purchases[record.partner_id][record.product_id.display_name] += record.product_uom_qty

    #     # Mettre à jour les enregistrements avec des données calculées
    #     for report in self:
    #         if report.partner_id:
    #             purchases = customer_purchases.get(report.partner_id, {})
    #             # Liste des produits
    #             report.customer_purchases = "\n".join(product_name for product_name in purchases.keys())
    #             # Liste des quantités
    #             report.customer_purchase_quantity = "\n".join(str(quantity) for quantity in purchases.values())
    #         else:
    #             report.customer_purchases = ""
    #             report.customer_purchase_quantity = ""


    @api.depends('partner_id', 'product_id', 'product_uom_qty')
    def _compute_customer_purchases(self):
        """ Regroupe les achats des clients par catégorie de produit et affiche les quantités totales. """
        # Regrouper les achats par client et par catégorie de produit
        customer_purchases_by_category = defaultdict(lambda: defaultdict(float))
        
        for record in self.env['sale.report'].search([]):
            if record.partner_id and record.product_id:
                # Récupérer la catégorie du produit
                category = record.product_id.categ_id.name
                # Additionner les quantités pour chaque produit dans chaque catégorie
                customer_purchases_by_category[record.partner_id][category] += record.product_uom_qty

        # Mettre à jour les enregistrements avec des données calculées
        for report in self:
            if report.partner_id:
                # Récupérer les achats du client pour chaque catégorie
                purchases = customer_purchases_by_category.get(report.partner_id, {})
                
                # Créer une chaîne de caractères pour afficher le nom du client, catégorie et quantité totale
                report.customer_purchases = "\n".join(
                    f"{category}" 
                    for category in purchases.keys()
                )
                
                # Créer une chaîne de caractères pour afficher la quantité totale pour chaque catégorie
                report.customer_purchase_quantity = "\n".join(
                    str(quantity) 
                    for quantity in purchases.values()
                )
            else:
                report.customer_purchases = ""
                report.customer_purchase_quantity = ""

