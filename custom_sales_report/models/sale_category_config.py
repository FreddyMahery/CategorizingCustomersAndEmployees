from odoo import models, fields

class SaleCategoryConfig(models.Model):

    # =================================== Private Attributes =====================

    _name = 'sale.category.config'
    _description = 'Configuration des seuils de catégories de vente'
    _sql_constraints = [
        (
            'threshold_quantity_check',  # Nom unique pour la contrainte
            'CHECK(threshold_quantity > 1)', 
            "Le seuil de quantité doit être strictement supérieur à 1."
        ),
        (
            'unique_partner_id',  # Nom unique pour la contrainte
            'UNIQUE(partner_id)', 
            "Une seule configuration est autorisée par client."
        ),
    ]

    # ====================================== Fields Declaration ===========================

    # Basic
    threshold_quantity = fields.Float(string='Seuil de Quantité', default=10.0,required=True)
    active = fields.Boolean(string='Actif', default=True)

    # Relational
    partner_id = fields.Many2one('res.partner', string='Client')
