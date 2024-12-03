# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import timedelta
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):

    # ================== Private Attributes ==================

    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price desc"
    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "The price must be strictly positive"),
    ]

    # ================== Fields Declaration =====================

    # Basic
    price = fields.Float(string="Price")
    # validide des offer et calcule de deadline
    validity = fields.Integer(string="Validity (days)", default=7)

    # Special
    state = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        string="Status",
        copy=False,
        default=False,
    )

    # Relation
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True, ondelete='cascade')
    # For stat button:
    property_type_id = fields.Many2one(
        "estate.property.type", 
        related="property_id.property_type_id", 
        string="Property Type", 
        store=True,
        # lier a la property par default en restrict
        ondelete='cascade',
    )

    # Computed
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    # ============================ Compute methode===================

    @api.depends("validity")
    def _compute_date_deadline(self):
        """
        Calculer la date limite en ajoutant validity à create_date.
        Si create_date n'est pas disponible, utiliser fields.Date.today() comme solution de secours.
        """
        for record in self:
            # Utiliser create_date s'il existe, sinon fallback sur la date actuelle
            base_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = base_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        """
        Mettre à jour la validité si l'utilisateur modifie directement la date limite.
        """
        for record in self:
            if record.date_deadline:
                base_date = record.create_date.date() if record.create_date else fields.Date.today()
                record.validity = (record.date_deadline - base_date).days
    
    # ======================== CRUD Methode =====================
    @api.model
    def create(self, vals):
        if vals.get("property_id") and vals.get("price"):
            prop = self.env["estate.property"].browse(vals["property_id"])

            # We check if the offer is higher than the existing offers
            if prop.offer_ids:
                max_offer = max(prop.mapped("offer_ids.price"))

                if (float_compare(vals["price"], max_offer, precision_rounding=0.01) <= 0):
                    raise UserError("The offer must be higher than %.2f" % max_offer)

            prop.state = "offer_received"

        return super().create(vals)

    # =================== Action Methode ===================

     #boutoons accepter et refuser
    def action_accept(self):
        if "accepted" in self.mapped("property_id.offer_ids.state"):
            raise UserError("An offer as already been accepted.")
        self.write(
            {
                "state": "accepted",
            }
        )
        return self.mapped("property_id").write(
            {
                "state": "offer_accepted",
                "selling_price": self.price,
                "buyer_id": self.partner_id.id,
            }
        )

    def action_refuse(self):
        return self.write(
            {
                "state": "refused",
            }
        )

    
    

