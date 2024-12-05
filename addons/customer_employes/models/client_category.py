from odoo import fields, models, api

class ClientCategory(models.Model):
    _name = 'client.category'
    _description = 'Client Tier Category'
    
    name = fields.Char(string='Catégorie', required=True)
    spending = fields.Monetary(string='Dépense minimum (MGA)', required=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.ref('base.MGA').id, required=True)

    @api.model
    def _get_default_currency(self):
        return self.env.ref('base.MGA').id

    def write(self, vals):
        res = super().write(vals)
        if 'spending' in vals:
            # Force le recalcul de la catégorie pour tous les clients
            self.env['res.partner'].search([])._compute_category()
        return res