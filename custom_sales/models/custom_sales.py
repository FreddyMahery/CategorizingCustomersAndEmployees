import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class CustomSales(models.Model):
    _name = 'custom.sales'
    _description = 'Custom Sales Module'

    @api.model
    def get_all_products(self, *args, **kwargs):
        """Récupère tous les produits enregistrés."""
        products = self.env['product.product'].search([])
        product_list = [{
            'name': product.name,
            'category': product.categ_id.name if product.categ_id else 'No Category',
            'price': product.list_price,
        } for product in products]

        # Log des produits
        _logger.info("Liste des produits : %s", product_list)

        return product_list

    @api.model
    def get_all_customers(self, *args, **kwargs):
        """Récupère tous les clients enregistrés."""
        customers = self.env['res.partner'].search([('is_customer', '=', True)])
        customer_list = [{
            'name': customer.name,
            'email': customer.email or 'No Email',
            'phone': customer.phone or 'No Phone',
        } for customer in customers]

        # Log des clients
        _logger.info("Liste des clients : %s", customer_list)

        return customer_list
