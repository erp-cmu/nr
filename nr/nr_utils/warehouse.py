import frappe
from nr.nr_utils.company import getFirstCompany


def getWarehousePK(name, company=None):
    if not company:
        company = getFirstCompany()

    warehouse_name_pk = None

    # Check primary key
    warehouse_name_pk = frappe.db.exists("Warehouse", name)
    if warehouse_name_pk:
        return warehouse_name_pk

    # Check primary key with company name
    warehouse_name_pk = frappe.db.exists("Warehouse", f"{name} - {company}")
    if warehouse_name_pk:
        return warehouse_name_pk

    # Check warehouse_name field
    warehouse_name_pk = frappe.db.exists(
        {"doctype": "Warehouse", "warehouse_name": name}
    )
    if warehouse_name_pk:
        return warehouse_name_pk

    return warehouse_name_pk


def getOrCreateWarehouse(
    warehouse_name,
    parent_warehouse=None,
    is_group=False,
    company=None,
):

    if not company:
        company = getFirstCompany()

    # Check existence
    warehouse_name_pk = frappe.db.exists("Warehouse", getWarehousePK(warehouse_name))
    if warehouse_name_pk:
        return warehouse_name_pk

    parent_warehouse_name_pk = None
    if parent_warehouse:
        parent_warehouse_name_pk = getWarehousePK(parent_warehouse)

    if parent_warehouse and not parent_warehouse_name_pk:
        frappe.throw("Parent warehouse does not exist.")

    doc = frappe.get_doc(
        {
            "doctype": "Warehouse",
            "warehouse_name": warehouse_name,
            "company": company,
            "is_group": is_group,
            "parent_warehouse": parent_warehouse_name_pk,
        }
    )

    doc.insert()
    return doc.name
