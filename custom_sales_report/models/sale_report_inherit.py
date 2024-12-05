# -*- coding: utf-8 -*-

from odoo import models, fields, api
from collections import defaultdict
import logging

_logger = logging.getLogger(__name__)
class CustomSaleReport(models.Model):

    # ================================ Pirvate Attributes ========================
    _inherit = 'sale.report'

    # =================================== Fields Declaration ===========================

    customer_purchases = fields.Text(string="Achats du client", compute="_compute_customer_purchases", store=False)
    customer_purchase_quantity = fields.Text(string="Quantité totale",compute="_compute_customer_purchases", store=False)
    predominant_category = fields.Char(string="Catégorie Prédominante", compute="_compute_predominant_category", store=False)

    # ==================================== Comput methods =====================
    
    @api.depends('partner_id', 'product_id', 'product_uom_qty')
    def _compute_customer_purchases(self):
        """ Regroupe les achats des clients en évitant les doublons pour chaque client. """
        # Regrouper les données par client et catégorie
        grouped_purchases = defaultdict(lambda: defaultdict(float))

        # Parcourir tous les enregistrements pour construire la structure des données
        for record in self.env['sale.report'].search([]):
            if record.partner_id and record.product_id:
                # Ajouter la quantité pour chaque catégorie de produit par client
                grouped_purchases[record.partner_id][record.product_id.categ_id.name] += record.product_uom_qty

        # Traiter les données pour chaque enregistrement
        processed_clients = set()  # Pour garder une trace des clients déjà affichés
        for report in self:
            if report.partner_id
                # Ajouter le client aux clients déjà affichés
                processed_clients.add(report.partner_id)

                # Récupérer les achats regroupés pour ce client
                purchases = grouped_purchases.get(report.partner_id, {})

                # Formater les catégories et quantités pour l'affichage
                report.customer_purchases = "\n".join(
                    f"{category}" for category in purchases.keys()
                )
                report.customer_purchase_quantity = "\n".join(
                    str(quantity) for quantity in purchases.values()
                )
            else:
                # Si aucun client associé, vider les champs
                report.customer_purchases = ""
                report.customer_purchase_quantity = ""

    @api.depends('partner_id', 'product_id', 'product_uom_qty')
    def _compute_predominant_category(self):
        """Calculer la catégorie prédominante en fonction des seuils de quantité"""
        for report in self:
            try:
                if report.partner_id:
                    # Récupérer la configuration active du seuil pour le client
                    config = self.env['sale.category.config'].search([
                        ('partner_id', '=', report.partner_id.id),
                        ('active', '=', True)
                    ], limit=1)

                    # Vérifier que le seuil existe et que la valeur est <= 1
                    if config and config.threshold_quantity < 1:
                        threshold = config.threshold_quantity
                    else:
                        threshold = 10.0  # Valeur par défaut si non valide ou inexistant

                    # Regrouper les achats par catégorie
                    category_quantities = defaultdict(float)
                    sales = self.env['sale.report'].search([('partner_id', '=', report.partner_id.id)])
                    for record in sales:
                        if record.product_id and record.product_id.categ_id:
                            category_quantities[record.product_id.categ_id.name] += record.product_uom_qty

                    # Filtrer les catégories selon le seuil
                    filtered_categories = {
                        category: quantity
                        for category, quantity in category_quantities.items()
                        if quantity >= threshold
                    }

                    # Déterminer la catégorie prédominante
                    if filtered_categories:
                        report.predominant_category = max(filtered_categories, key=filtered_categories.get)
                    else:
                        # Si aucune catégorie ne dépasse le seuil
                        report.predominant_category = "Non catégorisable"
                else:
                    # Aucun client associé
                    report.predominant_category = ""
            except Exception as e:
                # Gestion des erreurs et log de l'exception
                _logger.error(f"Erreur dans _compute_predominant_category : {e}")
                report.predominant_category = "Erreur"
