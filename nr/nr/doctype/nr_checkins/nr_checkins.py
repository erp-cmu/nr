# Copyright (c) 2024, IECMU and contributors
# For license information, please see license.txt

import frappe, os
from frappe.model.document import Document
import pandas as pd

class NRCheckins(Document):
        
    def after_insert(self):
        filepath = frappe.get_site_path() + self.excel
        if not os.path.exists(filepath):
            frappe.throw('Cannot find files')
        else:
            frappe.msgprint("OK")
			# pd.read_excel("sdfd.xlsx")
		# doc = frappe.new_doc("Item")
		# doc.item_code = "name3"
		# doc.item_name = "name3"
		# doc.item_group = "Products"
		# doc.insert()