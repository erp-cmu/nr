import frappe


def makeUOMFractional(uom_name):
    must_be_whole_number = frappe.db.get_value("UOM", uom_name, "must_be_whole_number")
    if must_be_whole_number:
        frappe.db.set_value("UOM", uom_name, "must_be_whole_number", 0)


def before_install():
    pass


def after_install():
    print("Processing after-install script.")

    # Make Nos fractional
    # NOTE: Unfortunately, ERPNext setup wizard overwrite this setting.
    makeUOMFractional(uom_name="Nos")

    # Disable rounded_total so that there is not problem with sales invoice and payment entry
    frappe.db.set_value(
        "Global Defaults", "Global Defaults", "disable_rounded_total", 1
    )

    # This method is dangerous since I do not know if other values are modified or not.
    # doc = frappe.get_doc("Global Defaults")
    # doc.disable_rounded_total = 1

    doc.insert()
