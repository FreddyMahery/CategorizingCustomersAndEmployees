from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    purchased_products = fields.Char(
        string="Products Purchased",
        compute="_compute_purchased_products",
        store=False  # Ce champ est calculé dynamiquement et n'est pas stocké en base.
    )

    @api.depends('sale_order_ids.order_line')
    def _compute_purchased_products(self):
        for partner in self:
            # Récupérer les produits achetés à partir des commandes validées
            orders = partner.sale_order_ids.filtered(lambda o: o.state in ['sale', 'done'])
            products = orders.mapped('order_line.product_id.name')
            partner.purchased_products = ', '.join(set(products)) if products else "Aucun produit"
