#-*- coding: utf-8 -*-

from odoo import models,fields, api

class EstatePropertyType(models.Model):

    # =================== Private Attributes ==============

    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "name"
    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The name must be unique"),
    ]

    # ======================== Fields Decaration ==================

    # Basic
    name = fields.Char(string="Property Name type", required=True)
    sequence = fields.Integer("Sequence", default=10)

    # Relational (for inline view)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")

    #  Computed (for stat button)
    offer_count = fields.Integer(string="Number of Offers", compute="_compute_offer_count")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")

    # ==================== Compute methods ===============
   
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
    