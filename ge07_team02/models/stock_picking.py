from odoo import api, fields, models
from datetime import datetime

class Picking(models.Model):
    _inherit = 'stock.picking'

    def _action_done(self):
        done = super()._action_done()
        if done and self.picking_type_id.sequence_code == 'OUT':
            for line in self.move_line_ids:
                if line.product_id.product_tmpl_id.detailed_type == 'motorcycle':
                    if self.origin:
                        sale_order = self.env['sale.order'].search([('name', '=', self.origin)], limit=1)
                        sale_order_id = sale_order[0].id if len(sale_order) > 0 else False
                    else:
                        sale_order_id = False
                    registered_motorcycle = self.env['motorcycle.registry'].create({
                        'vin': line.lot_id.name,
                        'current_mileage': 0.0,
                        'registry_date': datetime.now(),
                        'owner_id': self.partner_id.id,
                        'sale_order': sale_order_id
                    })
                    line.lot_id.registry_id = registered_motorcycle
        return done