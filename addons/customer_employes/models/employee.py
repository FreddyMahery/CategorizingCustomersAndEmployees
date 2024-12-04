from odoo import models, fields, api
from datetime import date
from dateutil.relativedelta import relativedelta

class Employee(models.Model):
    _inherit = 'hr.employee'

    monthly_sales = fields.Monetary(string="Ventes mensuelles", compute='_compute_monthly_sales', store=True, currency_field='company_currency_id')
    employee_category_id = fields.Many2one('employee.category', string='Catégorie employé', compute='_compute_employee_category', store=True)
    company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    
    @api.depends('user_id.sale_order_ids', 'user_id.sale_order_ids.state', 'user_id.sale_order_ids.amount_total')
    def _compute_monthly_sales(self):
        for employee in self:
            if not employee.user_id:
                employee.monthly_sales = 0
                continue

            current_month = date.today().replace(day=1)
            next_month = current_month + relativedelta(months=1)
            
            orders = employee.user_id.sale_order_ids.filtered(
                lambda o: o.state == 'sale' 
                and o.invoice_status == 'invoiced'
                and o.date_order >= current_month
                and o.date_order < next_month
            )
            
            employee.monthly_sales = sum(orders.mapped('amount_total'))

    @api.depends('monthly_sales')
    def _compute_employee_category(self):
        for employee in self:
            categories = self.env['employee.category'].search([])
            matched_category = employee.env['employee.category']
            highest_threshold = 0
            
            for category in categories:
                if employee.monthly_sales >= category.threshold and category.threshold >= highest_threshold:
                    matched_category = category
                    highest_threshold = category.threshold
                    
            employee.employee_category_id = matched_category
