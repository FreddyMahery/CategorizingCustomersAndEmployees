from odoo import models, fields

class EmployesHr(models.Model):
    _inherit = "hr.employee"

    #relation entre le categories employes
    #plusieurs employes un categories
    category_id = fields.Many2one('categories.employes', string='Performance Category')
