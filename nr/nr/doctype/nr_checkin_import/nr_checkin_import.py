# Copyright (c) 2024, IECMU and contributors
# For license information, please see license.txt

import frappe, os
from frappe.model.document import Document
from nr.nr_company.tor import processExcelTorDrink


class NRCheckinImport(Document):

    def run_checkins(self):
        COMPANY = frappe.conf.NR_COMPANY
        if not COMPANY:
            frappe.throw("Error getting company name settings")

        if not self.excel:
            frappe.throw(title="Error", msg="No file")

        filepath = frappe.get_site_path() + self.excel
        if not os.path.exists(filepath):
            frappe.throw(title="Error", msg="This file does not exist")

        if COMPANY == "tor":
            processExcelTorDrink(filepath=filepath)
            frappe.msgprint("Checkins Completed")
        else:
            frappe.throw("Error in setting company logic.")

    def after_insert(self):
        self.run_checkins()

    def on_change(self):
        self.run_checkins()
