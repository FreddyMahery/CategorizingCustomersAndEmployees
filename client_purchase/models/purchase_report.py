from odoo import models, fields, api

class ClientPurchaseReport(models.Model):
    _name = 'client.purchase.report'
    _description = 'Rapport des achats des clients'

    partner_id = fields.Many2one('res.partner', string='Client')
    product_name = fields.Char(string='Produit')
    quantity = fields.Float(string='Quantité Totale')

    @api.model
    def get_client_purchase_report(self):
        """
        Cette méthode récupère la liste des clients et leurs produits achetés avec les quantités totales.
        """
        SaleOrder = self.env['sale.order']
        report_data = []

        # Récupérer toutes les commandes de vente
        orders = SaleOrder.search([])  # Tous les ordres de vente dans le système
        for order in orders:
            for line in order.order_line:
                product_name = line.product_id.name
                quantity = line.product_uom_qty
                partner = order.partner_id

                # Ajouter les données dans le rapport
                existing = next((item for item in report_data if item['partner_id'] == partner.id and item['product_name'] == product_name), None)
                if existing:
                    existing['quantity'] += quantity
                else:
                    report_data.append({
                        'partner_id': partner.id,
                        'product_name': product_name,
                        'quantity': quantity,
                    })
        
        # Créer des enregistrements pour le rapport
        report_records = []
        for data in report_data:
            report_records.append((0, 0, {
                'partner_id': data['partner_id'],
                'product_name': data['product_name'],
                'quantity': data['quantity'],
            }))
        
        return report_records

    @api.model
    def refresh_report(self):
        """
        Supprime les anciens enregistrements et insère les nouveaux à partir des données consolidées.
        """
        # Supprime les anciens enregistrements
        self.search([]).unlink()

        # Récupère les nouvelles données
        new_data = self.get_client_purchase_report()

        # Crée les nouveaux enregistrements
        self.create(new_data)

