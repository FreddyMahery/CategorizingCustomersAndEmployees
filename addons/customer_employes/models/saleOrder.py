from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Relation avec l'employé responsable
    employee_id = fields.Many2one('hr.employee', string='Responsible Employee')
