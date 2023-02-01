# Copyright 2023 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64

from odoo import _, models
from odoo.exceptions import UserError

from odoo.addons.base.models.res_bank import sanitize_account_number


class AccountBankStatementImport(models.TransientModel):

    _inherit = 'account.bank.statement.import'

    def _find_additional_data(self, currency_code, account_number):

        journal_obj = self.env["account.journal"]
        for data_file in self.attachment_ids:
            if not self._check_ofx(base64.b64decode(data_file.datas)):
                return super()._find_additional_data(currency_code, account_number)

        if self.attachment_ids:
            sanitized_account_number = sanitize_account_number(account_number)
            journal = journal_obj.search(
                [
                    ("type", "=", "bank"),
                    (
                        "bank_account_id.sanitized_acctid",
                        "ilike",
                        sanitized_account_number,
                    ),
                ],
                limit=1,
            )
        journal_id = self.env.context.get("journal_id")
        if journal_id and journal.id != journal_id:
            raise UserError(
                _(
                    "The journal found for the file is not consistent with the "
                    "selected journal. You should use the proper journal or "
                    "use the generic button on the top of the Accounting Dashboard"
                )
            )
        if journal:
            account_number = journal.bank_acc_number

        return super()._find_additional_data(currency_code, account_number)
