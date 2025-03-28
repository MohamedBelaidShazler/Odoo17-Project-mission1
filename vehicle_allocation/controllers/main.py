from odoo import http
from odoo.http import request
from datetime import datetime

class VehicleController(http.Controller):

    @http.route('/', auth='public', website=True)
    def homepage(self):
        return request.render('vehicle_allocation.home_page')

    @http.route('/fleets', auth='public', website=True)
    def fleets_page(self, **kwargs):
        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')

        domaine = []

        contract_domain = []
        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

                contract_domain.append(('start_date', '<=', end_date))
                contract_domain.append(('expiration_date', '>=', start_date))

            except ValueError:
                return request.render('vehicle_allocation.fleets_page', {
                    'error': "Format de date invalide. Utilisez le format JJ/MM/AAAA."
                })

        today = datetime.today().date()
        contract_domain.append(('start_date', '<=', today))
        contract_domain.append(('expiration_date', '>=', today))

        contracts = request.env['fleet.vehicle.log.contract'].search(contract_domain)
        vehicles_with_contract = contracts.mapped('vehicle_id')

        vehicles_without_contract = request.env['fleet.vehicle'].search([
            ('id', 'not in', vehicles_with_contract.ids)
        ])

        return request.render('vehicle_allocation.fleets_page', {
            'vehicles_with_contract': vehicles_with_contract,
            'vehicles_without_contract': vehicles_without_contract,
            'start_date': start_date.strftime('%d/%m/%Y') if start_date else '',
            'end_date': end_date.strftime('%d/%m/%Y') if end_date else '',
        })

    @http.route('/car_details', auth='public', type='http', website=True)
    def step_two_page(self, car_id, **kwargs):
        start_date = request.params.get('start_date')
        end_date = request.params.get('end_date')

        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%d/%m/%Y').strftime('%Y-%m-%d')
            except ValueError:
                start_date = None  

        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%d/%m/%Y').strftime('%Y-%m-%d')
            except ValueError:
                end_date = None

        if not car_id or not car_id.isdigit():
            return request.render('website.404')

        car = request.env['fleet.vehicle'].sudo().browse(int(car_id))

        if car.exists():
            return request.render('vehicle_allocation.step_two_page', {
                'car': car,
                'start_date': start_date,
                'end_date': end_date
            })
        else:
            return request.render('website.404', {
                'error_message': "Désolé, ce véhicule n'existe pas ou a été supprimé."
            })

    @http.route('/contact', type='http', auth='public', website=True)
    def contact_page(self, **kwargs):
        return request.render('vehicle_allocation.contact_us_page')

    @http.route('/fleet-booking/create-reservation', type='http', auth='public', methods=['POST'], website=True)
    def create_reservation(self, **post):
        name = post.get('name')
        email = post.get('email')
        phone = post.get('phone')
        start_date_str = post.get('start_date')
        end_date_str = post.get('end_date')
        vehicle_id = int(post.get('vehicle_id'))

        partner = request.env['res.partner'].sudo().create({
            'name': name,
            'email': email,
            'phone': phone,
        })

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except Exception:
            return request.render('vehicle_allocation.error_template', {'error': 'Dates invalides.'})

        if end_date <= start_date:
            return request.render('vehicle_allocation.error_template',
                                  {'error': 'Date de fin doit être après la date de début.'})


        quotation = request.env['sale.order'].sudo().create({
            'partner_id': partner.id,
            'start_date': start_date,
            'end_date': end_date,
            'vehicle_id': vehicle_id,
            'note': f"Demande de réservation pour véhicule ID {vehicle_id}",
        })
        return request.render('vehicle_allocation.quotation_confirmation', {
            'partner': partner,
            'order': quotation,
            'start_date': start_date_str,
            'end_date': end_date_str,
        })
