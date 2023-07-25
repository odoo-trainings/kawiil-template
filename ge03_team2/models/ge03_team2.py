from odoo import api, fields, models

class Ge03Team2(models.Model):
    _inherit = 'product.template'
    
    name = fields.Char(compute="_compute_name", store = True)

    @api.depends("year","make","model","detailed_type")
    def _compute_name(self):
       
        for product in self.filtered(lambda r: r.detailed_type != "motorcycle"):
            self.name = self.name
        
        
        for product in self.filtered(lambda r: r.detailed_type == "motorcycle"):
            print(product)
            product.name = f"{product.year} {product.make} {product.model}"