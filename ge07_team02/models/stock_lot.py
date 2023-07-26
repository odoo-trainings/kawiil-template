from odoo import models, fields, api
from odoo.exceptions import ValidationError

class StockLot(models.Model):
    _inherit = "stock.lot"
    registry_id = fields.Many2one('motorcycle.registry', string='Motorcycle Registry')

    @api.constrains('registry_id')
    def _check_registry_id(self):
        for record in self:
            count = self.env['stock.lot'].search_count([('registry_id', '=', record.registry_id.id)])
            if count > 1:
                raise ValidationError('Odoopsie! A motorcycle registry can only be linked to one stock lot.')
