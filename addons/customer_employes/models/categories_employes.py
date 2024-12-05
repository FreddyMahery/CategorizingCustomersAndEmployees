from odoo import fields, models

class CategoriesEmployes(models.Model):
    _name = "categories.employes" 
    _description = "Employee Performance Category"

    name = fields.Char(string='Category Name', required=True)
    # Correction du champ One2many en spécifiant le bon inverse_name
    employee_ids = fields.One2many('hr.employee', 'category_id', string='Employees')
    min_threshold = fields.Float(string='Minimum Threshold', required=True, default=0)
    max_threshold = fields.Float(string='Maximum Threshold', required=True, default=0)