from odoo import fields,models,api

class ResPartner(models.Model):
    _inherit="res.partner"

    client_category_id=fields.Many2one('client.category',string='Catégorie Client')