import frappe
from nr.nr_utils.company import getFirstCompany
from nr.nr_utils.warehouse import getWarehousePK


def createStockEntryItemDict(
    item_code,
    qty,
    basic_rate=None,
):
    item = dict(item_code=item_code, qty=qty)
    if basic_rate:
        # valuation_rate does not seen to make a difference here, use basic_rate instead to speficy item cost
        item = {**item, "basic_rate": basic_rate}
    return item


def createStockEntry(to_warehouse, itemsDict, item_inout, company=None):

    if item_inout == "IN":
        stock_entry_type = "Material Receipt"
    elif item_inout == "OUT":
        stock_entry_type = "Material Issue"
    else:
        frappe.throw("Unknown item_inout")

    if not company:
        company = getFirstCompany()

    to_warehouse_name_pk = getWarehousePK(to_warehouse)
    if not to_warehouse_name_pk:
        frappe.throw("Unknown warehouse")

    entryDoc = frappe.get_doc(
        {
            "doctype": "Stock Entry",
            "docstatus": 1,
            "stock_entry_type": stock_entry_type,
            "company": company,
            "to_warehouse": to_warehouse_name_pk,
        }
    )

    for item in itemsDict:
        _ = entryDoc.append("items", {**item})
    entryDoc.insert()
