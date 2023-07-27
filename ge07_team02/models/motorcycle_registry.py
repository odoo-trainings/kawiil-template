from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class MotorcycleRegistry(models.Model):
    _inherit = "motorcycle.registry"

    stock_lot_ids = fields.One2many(
        'stock.lot',
        'registry_id',
        string='Stock Lots'
    )

    stock_name = fields.Char(
        related='stock_lot_ids.name'
    )

    sale_order = fields.Many2one('sale.order', string='Sale Order', readonly=True)

    @api.constrains('vin')
    def _check_vin_pattern(self):
        pattern = '^[A-Z]{4}\d{2}[A-Za-z0-9]{2}\d{5}$'
        for registry in self.filtered(lambda r: r.vin):
            match = re.match(pattern, registry.vin)
            if not match:
                raise ValidationError('Odoopsie! Invalid VIN')
            if not registry.vin[0:2] == 'KA':
                raise ValidationError('Odoopsie! Only motorcycles from Kauil Motors are allowed')

    @api.constrains('stock_lot_ids')
    def _check_stock_lot_ids(self):
        for record in self:
            if len(record.stock_lot_ids) > 1:
                raise ValidationError('Odoopsie! A motorcycle registry can only be linked to one stock lot.')