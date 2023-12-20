import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    env = api.Environment(cr, SUPERUSER_ID, {})
    asset_module = env["ir.module.module"].search([("name", "=", "account_asset")])
    if asset_module:
        asset_module.write({"auto_install": False})
