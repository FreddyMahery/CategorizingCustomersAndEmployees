from odoo import models, fields

class ResPartnerPurchase(models.Model):
    _name = 'res.partner.purchase'
    _description = 'Produits achetés par les clients'

    partner_id = fields.Many2one('res.partner', string='Client')
    product_name = fields.Char(string='Produit')
    quantity = fields.Float(string='Quantité Totale')
