from odoo import api, fields, models
from odoo.addons.http_routing.models.ir_http import slug


class MotorcycleRegistry(models.Model):
    _name = "motorcycle.registry"
    _inherit = ["portal.mixin", "motorcycle.registry"]

    def _get_portal_return_action(self):
        self.ensure_one()
        return self.env.ref("motorcycle_registry.registry_list_action")

    def _compute_access_url(self):
        super()._compute_access_url()
        for record in self:
            record.access_url = "/my/motorcycle/" + slug(self) + record.access_url
