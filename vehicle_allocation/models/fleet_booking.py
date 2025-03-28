from odoo import models, fields

class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'
    vehicle_image = fields.Image(string="Vehicle Image")
    price = fields.Float(string="Price")
    partner_id = fields.Many2one('res.partner', string="Partner", help="Le partenaire associé au véhicule")
    rental_contract_ids = fields.One2many('fleet.vehicle.log.contract', 'vehicle_id', string="Contrats de Location")