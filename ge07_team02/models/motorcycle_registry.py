from odoo import models, fields, api
from odoo.exceptions import ValidationError

class MotorcycleRegistry(models.Model):
    _inherit = "motorcycle.registry"

    stock_lot_ids = fields.One2many(
        'stock.lot',
        'registry_id',
        string='Stock Lots'
    )

    @api.constrains('stock_lot_ids')
    def _check_stock_lot_ids(self):
        for record in self:
            if len(record.stock_lot_ids) > 1:
                raise ValidationError('Odoopsie! A motorcycle registry can only be linked to one stock lot.')