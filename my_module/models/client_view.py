from odoo import models, fields

class ClientList(models.Model):
    _inherit = 'res.partner'

    # Champ calculé pour savoir si c'est un client
    is_customer = fields.Boolean(
        string="Est un Client",
        compute="_compute_is_customer",
        store=True,
    )

    def _compute_is_customer(self):
        for record in self:
            record.is_customer = record.customer_rank > 0

    
