from odoo import fields,models

class CategoriesEmployes(models.Model):
    _name = "categories.employes"
    _description = "Employee Performance Categor"


    name = fields.Char(string='Category Name', required=True)
    #relation entre le model employes 
    #un categorie plusieurs employes
    employee_ids = fields.One2many('hr.employee', 'category_id', string='Employees')