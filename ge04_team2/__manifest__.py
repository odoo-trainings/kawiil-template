{
    "name": "Motorcycle Discount",
    "summary": "Manage Registration of Motorcycles",
    "description": """
    Motorcycle Discount
====================
This Module creates a new pricelist with a discount of $2500.
Add a button that appears when it is the first time that the customer purchase a motorcycle.
This button only appears in quotations. 
When the button is pressed automatically the pricelist is applied to the motorcycles.
    """,
    "version": "1.0",
    "category": "Kauil/Discount",
    "license": "OPL-1",
    "depends": ["sale_management"],

    "data": [
        'data/discount_data.xml',
        'views/sale_order_inherit.xml'
    ],
    "author": "kauil-motors",
    "website": "www.odoo.com",
    "application": True,
}
