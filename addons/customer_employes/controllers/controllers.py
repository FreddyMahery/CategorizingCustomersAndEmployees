# -*- coding: utf-8 -*-
# from odoo import http


# class Tp2(http.Controller):
#     @http.route('/tp2/tp2', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tp2/tp2/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('tp2.listing', {
#             'root': '/tp2/tp2',
#             'objects': http.request.env['tp2.tp2'].search([]),
#         })

#     @http.route('/tp2/tp2/objects/<model("tp2.tp2"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tp2.object', {
#             'object': obj
#         })

