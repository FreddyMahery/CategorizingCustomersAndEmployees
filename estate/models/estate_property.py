# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):

    # ===================== Private Attributes ===============
    _name = "estate.property"
    _description  = "Estate Property"
    _order = "id desc"
    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)", "The expected price must be strictly positive"),
        ("check_selling_price", "CHECK(selling_price >= 0)", "The offer price must be positive"),
    ]

    # ============================ Default Methods =================

    def _default_availability_date(self):
        return (datetime.today() + timedelta(days=90)).date()

    # ========================== Fields Declaration ===================

    # Basic
    name = fields.Char(string="Property Name", required=True, default="Unknown")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Date of Availability", copy=False, default=_default_availability_date)
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Number of Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Number of Facades")
    garage = fields.Boolean(string="Has Garage?")
    garden = fields.Boolean(string="Has Garden?")
    garden_area = fields.Integer(string="Garden Area (sqm)", ndefault=0)
    
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string="Garden Orientation"
    )

    # Special
    # Définition du champ "state"
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ],
        string="Status",
        default='new',
        required=True,
        copy=False,
    )

    active = fields.Boolean(string="Active", default=True)

     
    # Relation entre les models
    # many2one relation
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    # Ajout des champs pour le vendeur et l'acheteur
    user_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user, required=True)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False, readonly=True)
    tag_ids = fields.Many2many(
        "estate.property.tag",  # Modèle cible
        string="Tags"         # Nom affiché dans l'interface
        )
    #One2many
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    # champ calculer
    # totoal area
    total_area = fields.Float(compute="_compute_total", string="Total Area (sqm)")
     # best price
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")

    # ============================== Compute methode ===================

    @api.depends("garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
   
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            # Utiliser mapped() pour récupérer les prix et max() pour trouver le maximum
            # record.best_price = max(record.offer_ids.mapped('price'), default=0.0)
            record.best_price = max(record.offer_ids.mapped("price")) if record.offer_ids else 0.0

    # ================= Contrains and Onchanges ===================

    @api.constrains("expected_price", "selling_price")
    def _check_price_difference(self):
        for prop in self:
            if (
                not float_is_zero(prop.selling_price, precision_rounding=0.01)
                and float_compare(prop.selling_price, prop.expected_price * 90.0 / 100.0, precision_rounding=0.01) < 0
            ):
                raise ValidationError(
                    "The selling price must be at least 90% of the expected price! "
                    + "You must reduce the expected price if you want to accept this offer."
                )

    @api.onchange('garden')
    def _onchange_garden(self):
        """
        Définit les valeurs par défaut pour garden_area et garden_orientation
        lorsque garden est activé. Réinitialise les champs lorsque garden est désactivé.
        """
        if self.garden:
            self.garden_area = 10  # Superficie par défaut
            self.garden_orientation = 'north'  # Orientation par défaut
        else:
            self.garden_area = 0  # Réinitialisation
            self.garden_orientation = False  # Réinitialisation

    # ========================= CRUD Methods ==================

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_canceled(self):
        if not set(self.mapped("state")) <= {"new", "canceled"}:
            raise UserError("Only new and canceled properties can be deleted.")
    
    # =================== Action Methods =======================

    def action_sold(self):
        if "canceled" in self.mapped("state"):
            raise UserError("Canceled properties cannot be sold.")
        return self.write({"state": "sold"})

    def action_cancel(self):
        if "sold" in self.mapped("state"):
            raise UserError("Sold properties cannot be canceled.")
        return self.write({"state": "canceled"})

   
    
    
    
