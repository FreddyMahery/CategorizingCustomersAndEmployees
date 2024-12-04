from odoo import fields, models, api
from datetime import date
from dateutil.relativedelta import relativedelta

class ResPartner(models.Model):
    _inherit = 'res.partner'

    monthly_spending = fields.Monetary(
        string="Dépense mensuelle", 
        compute='_compute_monthly_spending', 
        store=True, 
        currency_field='currency_id'  # Changement ici - utiliser currency_id au lieu de company_currency_id
    )
    client_category_id = fields.Many2one('client.category', string="Catégorie client", compute='_compute_category', store=True)
    currency_id = fields.Many2one(
        'res.currency', 
        string='Currency',
        related='property_product_pricelist.currency_id',
        readonly=True
    )

    @api.depends('invoice_ids', 'invoice_ids.state', 'invoice_ids.amount_total')
    def _compute_monthly_spending(self):
        mga_currency = self.env.ref('base.MGA')
        for partner in self:
            current_month = date.today().replace(day=1)
            next_month = current_month + relativedelta(months=1)
            invoices = partner.invoice_ids.filtered(
                lambda inv: inv.state == 'posted' 
                and inv.move_type == 'out_invoice'
                and inv.invoice_date >= current_month 
                and inv.invoice_date < next_month
            )
            total = 0
            for invoice in invoices:
                # Conversion en MGA
                amount_mga = invoice.currency_id._convert(
                    invoice.amount_total_signed,
                    mga_currency,
                    partner.company_id,
                    invoice.date
                )
                total += amount_mga
            partner.monthly_spending = total

    @api.depends('monthly_spending')
    def _compute_category(self):
        for partner in self:
            categories = self.env['client.category'].search([], order='spending ASC')
            partner.client_category_id = False
            
            # Si le client n'a pas de dépenses, on ne lui attribue pas de catégorie
            if not partner.monthly_spending:
                continue
                
            # Parcours des catégories pour trouver la plus appropriée
            for category in categories:
                if partner.monthly_spending >= category.spending:
                    partner.client_category_id = category
