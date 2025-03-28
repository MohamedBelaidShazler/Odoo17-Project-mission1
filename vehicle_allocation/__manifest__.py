{
    'name': 'Vehicle Allocation System',
    'version': '17.0.1.0.0',
    'category': 'Website',
    'summary': 'Manage vehicle allocation via the website',
    'author': 'Mohamed Belaid',
    'depends': ['website', 'fleet', 'sale'],
    'data': [
        'views/homepage_view.xml',
         'views/navbar.xml',
        'views/fleets_page_add.xml',
        'views/fleets_view.xml',
        'views/step_two_view.xml',
        'views/contact_view.xml',
        'views/footer.xml',
        'views/contact_confirmation_template.xml',
        'views/sales_qota_add.xml',
        'views/quotation_confirmation.xml',
        'data/website_menu.xml'

    ],
    'controllers': [
        'controllers/main.py',

    ],
    'installable': True,
    'auto_install': False,
    'application': True
}
