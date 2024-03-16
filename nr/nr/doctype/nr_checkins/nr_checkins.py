# Copyright (c) 2024, IECMU and contributors
# For license information, please see license.txt

import frappe, os
from frappe.model.document import Document
import pandas as pd

from nr.nr.doctype.nr_checkins.utils import processExcelTorDrink, createCheckins


class NRCheckins(Document):

    def after_insert(self):
        filepath = frappe.get_site_path() + self.excel
        if not os.path.exists(filepath):
            frappe.throw("Cannot find files")
        else:
            frappe.msgprint("OK")
            df = processExcelTorDrink(filepath=filepath)
            df.apply(lambda row: createCheckins(**row.to_dict()), axis=1)


# pd.read_excel("sdfd.xlsx")
