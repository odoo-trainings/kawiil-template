from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    name = fields.Char(compute="_compute_name", store = True)

    @api.depends("year","make","model","detailed_type")
    def _compute_name(self):
        for product in self:
            if product.detailed_type == "motorcycle":
                product.name = f"{product.year} {product.make} {product.model}"
            else:
                self.name = self.name
                