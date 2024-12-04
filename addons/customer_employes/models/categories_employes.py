from odoo import fields,models

class CategoriesEmployes(models.Model):
    _name = "categories.employes" 
    _description = "Employee Performance Categor"


    name = fields.Char(string='Category Name', required=True)
    #relation entre le model employes 
    #un categorie plusieurs employes
    employee_ids = fields.One2many('hr.employee', 'category_id', string='Employees')
    min_threshold = fields.Float(string='Minimum Threshold',required=True,default = 0)  # Montant minimum pour cette catégorie
    max_threshold = fields.Float(string='Maximum Threshold',required=True,default = 0)  # Montant maximum pour cette catégorie