from odoo import fields, models,api

class ClientCategory(models.Model):
    _name = 'client.category'
    _description = 'Client Tier Category'
    _inherit='res.partner.category'
    name = fields.Char(string='Catégorie', required=True)
    spending = fields.Float(string='Dépense minimum', required=True)