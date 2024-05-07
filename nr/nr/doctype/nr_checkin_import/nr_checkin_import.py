# Copyright (c) 2024, IECMU and contributors
# For license information, please see license.txt

import frappe, os
from frappe.model.document import Document
from nr.nr_services.checkin_import.tor import processExcelTorDrink
from nr.nr_services.checkin_import.nakorn import processExcelNakorn


class NRCheckinImport(Document):

    def run_checkins(self):
        COMPANY = frappe.conf.NR_COMPANY
        if not COMPANY:
            frappe.throw("No NR_COMPANY value. Specify NR_COMPANY in site_config.json")

        if not self.excel:
            frappe.throw(title="Error", msg="No file")

        filepath = frappe.get_site_path() + self.excel
        if not os.path.exists(filepath):
            frappe.throw(title="Error", msg="This file does not exist")

        if COMPANY == "tor":
            processExcelTorDrink(
                filepath=filepath, default_shift_type=self.default_shift_type
            )
            frappe.msgprint("Checkins Completed")
        elif COMPANY == "nakorn":
            processExcelNakorn(
                filepath=filepath, default_shift_type=self.default_shift_type
            )
        else:
            frappe.throw("Error in setting company logic.")

    def after_insert(self):
        self.run_checkins()

    # def on_change(self):
    #     self.run_checkins()
