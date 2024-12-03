from odoo import fields,models,api
from datetime import date
from dateutil.relativedelta import relativedelta
class ResPartner(models.Model):
    _inherit="res.partner"
    monthly_spending =fields.Float(string="Dépense par mois (MGA)",compute='_compute_monthly_spending',store=True)
    client_category_id=fields.Many2one('client.category',string='Catégorie Client',compute='_compute_category')

    @api.depends('invoice_ids.amount_total','invoice_ids.currency_id')
    def _compute_monthly_spending(self):
        for partner in self:
            current_month = date.today().replace(day=1)
            end_month=current_month + relativedelta(months=1)
            total_spending=0
            invoices = partner.invoice_ids.filtered(lambda inv: inv.state=="posted" and inv.move_type=="out_invoice" and inv.invoice_date>= current_month and inv.invoice_date<=end_month)
            for invoice in invoices:
                if invoice.currency_id != self.env.company.currency_id:
                    total_mga = invoice.currency_id._convert(invoice.amount_total,self.env.company.currency_id,self.env.company,invoice.invoice_date or fields.Date.today())
                else:
                    total_mga=invoice.amount_total

                total_spending += total_mga
            partner.monthly_spending = total_spending
            

    @api.depends('monthly_spending')
    def _compute_category(self):
        for partner in self:
            categories = self.env['client.category'].search([])
            for partner in self:
                best_category = None
                for category in categories:
                    if partner.monthly_spending >= category.spending:
                        if not best_category or category.spending > best_category.spending:
                            best_category = category
                partner.client_category_id = best_category
