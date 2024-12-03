from odoo import models, fields, api

class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    product_purchases = fields.One2many('res.partner.purchase', 'partner_id', string='Achats')

    @api.onchange('id')
    def _compute_product_purchases(self):
        """
        Calcule les produits achetés par le client et leurs quantités totales.
        """
        SaleOrder = self.env['sale.order']
        ProductPurchase = self.env['res.partner.purchase']

        for partner in self:
            product_quantities = {}

            # Récupérer toutes les commandes du client
            orders = SaleOrder.search([('partner_id', '=', partner.id)])
            for order in orders:
                for line in order.order_line:
                    product_name = line.product_id.name
                    quantity = line.product_uom_qty

                    if product_name in product_quantities:
                        product_quantities[product_name] += quantity
                    else:
                        product_quantities[product_name] = quantity

            # Mettre à jour les achats dans le modèle `res.partner.purchase`
            ProductPurchase.search([('partner_id', '=', partner.id)]).unlink()  # Supprime les anciens enregistrements
            for product_name, total_quantity in product_quantities.items():
                ProductPurchase.create({
                    'partner_id': partner.id,
                    'product_name': product_name,
                    'quantity': total_quantity,
                })
