from odoo import http
from odoo.http import request
from odoo.osv.expression import AND, OR

from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.exceptions import AccessError, MissingError, ValidationError


class MotorcycleRegistryPortal(portal.CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id
        MotorcycleRegistry = request.env["motorcycle.registry"]
        if "motorcycle_registry_count" in counters:
            values["motorcycle_registry_count"] = (
                MotorcycleRegistry.search_count(
                    self._prepare_motorcycle_registry_domain(partner)
                )
                if MotorcycleRegistry.check_access_rights("read", raise_exception=False)
                else 0
            )
        return values

    def _prepare_search_domain(self, search, search_in):
        search_domain = []
        if search:
            if search_in in ("all", "registry_number"):
                search_domain = OR(
                    [search_domain, [("registry_number", "ilike", search)]]
                )
            if search_in in ("all", "license_plate"):
                search_domain = OR(
                    [search_domain, [("license_plate", "ilike", search)]]
                )
            if search_in in ("all", "vin"):
                search_domain = OR([search_domain, [("vin", "ilike", search)]])
        return search_domain

    def _prepare_motorcycle_registry_domain(
        self, partner, search_in="all", search=None
    ):
        search_domain = [("owner_id", "=", partner.id)]

        search_domain = AND(
            [search_domain, self._prepare_search_domain(search, search_in)]
        )

        return search_domain

    def _prepare_motorcycle_portal_rendering_values(self, page=1, **kwargs):
        MotorcycleRegistry = request.env["motorcycle.registry"]
        url = "/my/motorcycle"
        partner = request.env.user.partner_id
        values = self._prepare_portal_layout_values()
        domain = self._prepare_motorcycle_registry_domain(
            partner,
            search=kwargs.get("search", None),
            search_in=kwargs.get("search_in", "all"),
        )

        pager_values = portal_pager(
            url=url,
            total=MotorcycleRegistry.search_count(domain),
            page=page,
            step=self._items_per_page,
        )

        motorcycles = MotorcycleRegistry.search(
            domain, limit=self._items_per_page, offset=pager_values["offset"]
        )

        values.update(
            {
                "motorcycles": motorcycles.sudo(),
                "page_name": "motorcycle",
                "pager": pager_values,
                "default_url": url,
            }
        )

        return values

    @http.route(
        ["/my/motorcycles", "/my/motorcycles/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_motorcycles(self, search=None, search_in="all", **kwargs):
        searchbar_inputs = {
            "all": {"label": "Search in All", "input": "all"},
            "registry_number": {
                "label": "Search in Registry Number",
                "input": "registry_number",
            },
            "vin": {"label": "Search in VIN", "input": "vin"},
            "license_plate": {
                "label": "Search in License Plate",
                "input": "license_plate",
            },
        }

        values = self._prepare_motorcycle_portal_rendering_values(
            search=search, search_in=search_in, **kwargs
        )

        values.update({"searchbar_inputs": searchbar_inputs, "search_in": search_in})
        request.session["motorcycles"] = values["motorcycles"].ids[:100]
        return request.render("ge08_team02.portal_my_motorcycles_registry", values)

    @http.route(
        ['/my/motorcycle/<model("motorcycle.registry"):motorcycle>'],
        type="http",
        auth="user",
        website=True,
    )
    def portal_motorcycle_page(
        self, motorcycle, access_token=None, message=False, download=False, **kw
    ):
        try:
            motorcycle_sudo = self._document_check_access(
                "motorcycle.registry", motorcycle.id, access_token=access_token
            )
        except (AccessError, MissingError):
            return request.redirect("/my")
        backend_url = (
            f"/web#model={motorcycle_sudo._name}"
            f"&id={motorcycle_sudo.id}"
            f"&action={motorcycle_sudo._get_portal_return_action().id}"
            f"&view_type=form"
        )
        values = {
            "motorcycle": motorcycle_sudo,
            "message": message,
            "report_type": "html",
            "backend_url": backend_url,
        }

        values = self._get_page_view_values(
            motorcycle_sudo, access_token, values, "motorcycle", False
        )

        return request.render("ge08_team02.motorcycle_portal_template", values)
