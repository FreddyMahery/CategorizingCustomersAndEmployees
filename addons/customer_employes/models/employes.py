from odoo import models, fields, api

class EmployesHr(models.Model):
    _inherit = 'hr.employee'

    category_id = fields.Many2one('categories.employes', string='Performance Category')
    total_managed_amount = fields.Float(string='Total Managed Amount', compute='_compute_total_managed_amount', store=True)
    related_orders = fields.One2many('sale.order', 'employee_id', string='Orders Managed')

    @api.depends('related_orders')
    def _compute_total_managed_amount(self):
        """
        Calcule le montant total des commandes gérées par chaque employé.
        """
        for employee in self:
            employee.total_managed_amount = sum(
                order.amount_total for order in employee.related_orders if order.state == 'sale'
            )

    @api.model
    def categorize_employees(self):
        """
        Assigne une catégorie à chaque employé en fonction du total des commandes gérées.
        """
        categories = self.env['categories.employes'].search([])
        for employee in self.search([]):
            # Cherche la catégorie correspondant au montant total géré
            category = categories.filtered(lambda c: c.min_threshold <= employee.total_managed_amount < c.max_threshold)
            if category:
                employee.category_id = category[0].id  # Assigne la première catégorie trouvée
