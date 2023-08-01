{
    "name": "ge03_team2",
    
    "summary": "Manage Registration of Motorcycles",
    
    "description": """
    Motorcycle Registry
====================
This Module is used for ge03 internship excercise: the goal of this module is that whenever a new motorcycle
type product is created the name of the motorcycle changes into the format 'year make model'
this means that any other type of product that is not a motorcycle must not be affected by this change.
To do this the name field is going to be computed whenever is validated that the product is actually a motorcycle
    """,
    
    "version": "1.0.0",
    
    "category": "Kauil/Registry",
    
    "license": "OPL-1",
    
    "depends": ["stock", 
                "website", 
                "motorcycle_registry"
                ],
    
    "author": "kauil-motors",
    
    "website": "www.odoo.com",
    
    "application": True,
    
}