from odoo import fields,models,api
from datetime import date
from dateutil.relativedelta import relativedelta
class ResPartner(models.Model):
    _inherit="res.partner"
    monthly_spending =fields.Float(string="Dépense par mois",compute='_compute_monthly_spending')
    client_category_id=fields.Many2one('client.category',string='Catégorie Client',compute='_compute_category')

    @api.depends('invoice_ids.amount_total')
    def _compute_monthly_spending(self):
        for partner in self:
            current_month = date.today().replace(day=1)
            end_month=current_month + relativedelta(months=1)

            invoices = partner.invoice_ids.filtered(lambda inv: inv.state=="posted" and inv.move_type=="out_invoice" and inv.invoice_date>= current_month and inv.invoice_date<=end_month)
            partner.monthly_spending = sum(invoices.mapped('amount_total'))

    @api.depends('monthly_spending')
    def _compute_category(self):
        for partner in self:
            categories = self.env['client.category'].search([])

            for category in categories:
                if partner.monthly_spending >= category.spending:
                    partner.client_category_id= category
