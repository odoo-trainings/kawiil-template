from odoo import api, fields, models
from datetime import datetime

class Picking(models.Model):
    _inherit = 'stock.picking'

    def _action_done(self):
        done = super()._action_done()
        if done and self.picking_type_id.sequence_code == 'OUT':
            for line in self.move_line_ids:
                if line.product_id.product_tmpl_id.detailed_type == 'motorcycle':
                    registered_motorcycle = self.env['motorcycle.registry'].create({
                        'vin': line.lot_id.name,
                        'current_mileage': 0.0,
                        'registry_date': datetime.now(),
                        'owner_id': self.partner_id.id
                    })
                    line.lot_id.registry_id = registered_motorcycle
        return done