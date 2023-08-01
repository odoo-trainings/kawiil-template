from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_new_customer = fields.Boolean(compute="_compute_first_purchase")

    @api.depends('partner_id')
    def _compute_first_purchase(self):
        for record in self:
            sale_orders = self.env['sale.order'].search(
                [('partner_id', '=', record.partner_id.id)])
            order_lines = sale_orders.filtered(
                lambda r: r.state == 'sale').mapped('order_line')
            record.is_new_customer = False if len(order_lines.mapped('product_id').filtered(
                lambda product: product.detailed_type == 'motorcycle'
            )) > 0 else True

    def change_pricelist(self):
        for record in self:
            record.pricelist_id = self.env.ref(
                'ge04_team2.discount_first_purchase')
            self.action_update_prices()

    def action_update_prices(self):
        if (self.pricelist_id == self.env.ref(
                'ge04_team2.discount_first_purchase') and self.is_new_customer == False):
            raise ValidationError("You are not a new customer")
        super().action_update_prices()

    def _get_update_prices_lines(self):
        """ Hook to exclude specific lines which should not be updated based on price list recomputation """
        return self.order_line.filtered(lambda line: line.product_type == "motorcycle")
