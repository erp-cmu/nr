import frappe
import datetime


def handleShiftAssignment(emp_name, default_shift_type):

    SA_name = frappe.db.exists("Shift Assignment", {"employee": emp_name})

    if SA_name:
        shift_type = frappe.db.get_value("Shift Assignment", SA_name, "shift_type")
        return shift_type
    else:
        year = datetime.date.today().year
        start_date = datetime.datetime(year, 1, 1)

        doc = frappe.get_doc(
            {
                "doctype": "Shift Assignment",
                "employee": emp_name,
                "docstatus": 1,
                "shift_type": default_shift_type,
                "start_date": start_date,
            }
        )
        newSA = doc.insert()
        return default_shift_type
