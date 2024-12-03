#-*- coding: utf-8 -*-

from odoo import models,fields

class EstatePropertyTag(models.Model):

    # ================== Private Attributes================

    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"
    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The name must be unique"),
    ]

    # ======================= Fields Declaration ===================

    # Basic
    name = fields.Char(string="Property Tag", required=True)
    color = fields.Integer("Color Index")
