from odoo import api, fields, models


class ge04Team2(models.Model):
    _inherit = 'sale.order'

    is_new_customer = fields.Boolean(compute="_compute_first_purchase")

    @api.depends('partner_id')
    def _compute_first_purchase(self):
        for record in self:
            record.is_new_customer = True

            partner = record.partner_id.id
            sale_orders = self.env['sale.order'].search(
                [('partner_id', '=', partner)])

            order_lines = sale_orders.filtered(
                lambda r: r.type_name == 'Sales Order').mapped('order_line')

            products = order_lines.mapped('product_id')

            print(products)

            for i in products:
                print(i.detailed_type)
                if i.detailed_type == "motorcycle":
                    record.is_new_customer = False

    def change_pricelist(self):
        for record in self:
            record.pricelist_id = self.env.ref(
                'ge04_team2.discount_first_purchase')
            self.action_update_prices()

    def _get_update_prices_lines(self):
        """ Hook to exclude specific lines which should not be updated based on price list recomputation """
        return self.order_line.filtered(lambda line: line.product_type == "motorcycle")
