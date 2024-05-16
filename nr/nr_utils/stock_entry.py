import frappe
from nr.nr_utils.company import getFirstCompany
from nr.nr_utils.warehouse import getWarehousePK
from nr.nr_utils.common import date_parse
from datetime import datetime


def createStockEntryItemDict(
    item_code,
    qty,
    uom="Nos",
    basic_rate=None,
):
    item = dict(item_code=item_code, qty=qty, uom=uom)
    if basic_rate:
        # valuation_rate does not seen to make a difference here, use basic_rate instead to speficy item cost
        item = {**item, "basic_rate": basic_rate}
    return item


def createStockEntry(
    itemsDict,
    item_inout,
    to_warehouse=None,
    from_warehouse=None,
    company=None,
    posting_date=None,
):

    print("Posting Date", posting_date)
    if not posting_date:
        posting_date = datetime.now()
    elif type(posting_date) is str:
        try:
            posting_date = date_parse(posting_date)
        except:
            frappe.throw("Cannot parse date string.")
    else:
        frappe.throw("Invalid posting_Date")

    if item_inout == "IN":
        stock_entry_type = "Material Receipt"
        if not to_warehouse:
            frappe.throw(msg="Need to_warehouse")
    elif item_inout == "OUT":
        stock_entry_type = "Material Issue"
        if not from_warehouse:
            frappe.throw(msg="Need from_warehouse")
    else:
        frappe.throw("Unknown item_inout")

    if not company:
        company = getFirstCompany()

    if to_warehouse:
        to_warehouse_name_pk = getWarehousePK(to_warehouse)
        if not to_warehouse_name_pk:
            frappe.throw(f"Unknown warehouse: {to_warehouse_name_pk}")

    if from_warehouse:
        from_warehouse_name_pk = getWarehousePK(from_warehouse)
        if not from_warehouse_name_pk:
            frappe.throw(f"Unknown warehouse: {from_warehouse_name_pk}")

    # Check for valid item
    for item in itemsDict:
        item_code = item["item_code"]
        item_name_pk = frappe.db.exists("Item", {"item_code": item_code})
        if not item_name_pk:
            frappe.throw(msg=f"Cannot find item: {item_code}")

    docData = {
        "stock_entry_type": stock_entry_type,
        "company": company,
        "posting_date": posting_date,
        "set_posting_time": True,
    }
    if item_inout == "IN":
        docData["to_warehouse"] = to_warehouse_name_pk
    elif item_inout == "OUT":
        docData["from_warehouse"] = from_warehouse_name_pk

    entryDoc = frappe.get_doc({"doctype": "Stock Entry", "docstatus": 1, **docData})

    for item in itemsDict:
        _ = entryDoc.append("items", {**item})
    entryDoc.insert()
