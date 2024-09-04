# Copyright (c) 2024, IECMU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from nr.nr_services.sales_import import processExcelAutoSalesFile
from nr.nr_services.sales_import_steel import processXMLSteel
import frappe, os


class NRSalesImport(Document):

    def run_import_item(self):
        if not self.excel:
            frappe.throw(title="Error", msg="No file")
        filepath = frappe.get_site_path() + self.excel
        if not os.path.exists(filepath):
            frappe.throw(title="Error", msg="This file does not exist")

        COMPANY = frappe.conf.NR_COMPANY        
        if not COMPANY:
            frappe.throw("No NR_COMPANY value. Specify NR_COMPANY in site_config.json")

        if COMPANY == "steel":
            processXMLSteel(filepath=filepath)            
        else:
            processExcelAutoSalesFile(filepath=filepath)

    def after_insert(self):
        self.run_import_item()
