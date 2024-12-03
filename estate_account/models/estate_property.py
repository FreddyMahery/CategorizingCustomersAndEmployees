# -*- coding: utf-8 -*-

from odoo import models, api, fields
from odoo import Command

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        # Ajoutez un message pour tester si la méthode est appelée
        # print("action_sold called from estate_account module")
        # Vous pouvez également placer un point d'arrêt pour le débogage
        # import pdb; pdb.set_trace()
        
        # Appel à la méthode d'origine
        
        # return super().action_sold()


        # Appeler la méthode `action_sold` de la superclasse
        res = super().action_sold()
        
        # Récupérer le journal des ventes
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        
        if not journal:
            raise UserError("No sales journal found. Please configure one.")

        # Parcourir les propriétés marquées comme "vendues"
        for prop in self:
            # Vérifier qu'un acheteur est associé à la propriété
            if not prop.buyer_id:
                raise UserError("A buyer must be set before selling the property.")

            # Étape 1 : Créer une facture vide
            invoice = self.env["account.move"].create({
                "partner_id": prop.buyer_id.id,  # Tiré de la propriété en cours
                "move_type": "out_invoice",     # Type de facture client
                "journal_id": journal.id,       # Journal des ventes
            })

            # Étape 2 : Ajouter les lignes de facture (invoice_line_ids)
            invoice.write({
                "invoice_line_ids": [
                    Command.create({
                        "name": prop.name,  # Nom de la propriété
                        "quantity": 1.0,    # Quantité (1 unité)
                        "price_unit": prop.selling_price * 6.0 / 100.0,  # Commission de 6%
                    }),
                    Command.create({
                        "name": "Administrative fees",  # Frais administratifs
                        "quantity": 1.0,                # Quantité (1 unité)
                        "price_unit": 100.0,            # Montant fixe pour les frais
                    }),
                ]
            })
        
        return res
            
        