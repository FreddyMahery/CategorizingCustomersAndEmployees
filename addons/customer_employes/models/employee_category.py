from odoo import models, fields, api

class EmployeeCategory(models.Model):
    _name = 'employee.category'
    _description = 'Catégorie employé'

    name = fields.Char('Nom', required=True)
    threshold = fields.Monetary('Seuil mensuel', required=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id.id)
    description = fields.Text('Description')
