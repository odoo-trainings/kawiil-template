{
    "name": "Motorcycle Discount",
    "summary": "Manage Registration of Motorcycles",
    "description": """
    Motorcycle Discount
====================
This Module is used to show a discount when a new customer purchase a motorcycle in them first time.
    """,
    "version": "0.1",
    "category": "Kauil/Discount",
    "license": "OPL-1",
    "depends": ["sale_management"],

    "data": [
        'data/discount_data.xml',
        'views/sale_order_inherit.xml'
    ],
    "demo": [],
    "author": "kauil-motors",
    "website": "www.odoo.com",
    "application": True,
}
