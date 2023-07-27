from odoo import api, fields, models


class StockLot(models.Model):
    _inherit = "stock.lot"

    @api.model
    def _get_next_serial(self, company, product):
        last_serial = self.env["stock.lot"].search(
            [("company_id", "=", company.id), ("product_id", "=", product.id)],
            limit=1,
            order="id DESC",
        )
        if product.product_tmpl_id.detailed_type == "motorcycle":
            make = product.make if product.make else "XX"
            model = product.model if product.model else "XX"
            year = str(product.year) if product.year else "00"
            battery = product.battery_capacity if product.battery_capacity else "xl"
            serial = make + model + year + battery
            if not last_serial:
                return "{}{}".format(serial, "00001")
            else:
                return self.env["stock.lot"].generate_lot_names(last_serial.name, 2)[1]
        else:
            super()._get_next_serial(company, product)
