from odoo import models, fields

class SalesQota(models.Model):

    _inherit = 'sale.order'
    start_date = fields.Date()
    end_date = fields.Date()
    vehicle_id = fields.Many2one('fleet.vehicle')

