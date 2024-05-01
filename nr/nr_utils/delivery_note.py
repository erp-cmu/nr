import frappe
from nr.nr_utils.customer import getOrCreateCustomer
from nr.nr_utils.common import date_parse


def createDeliveryNoteItemDict(
    item_code,
    qty,
    rate,
    against_sales_order=None,
    so_detail=None,
    against_sales_invoice=None,
    si_detail=None,
    uom="Nos",
):

    billed_amt = qty * rate
    item = dict(item_code=item_code, qty=qty, rate=rate, uom=uom, billed_amt=billed_amt)

    if against_sales_order and so_detail:
        item["against_sales_order"] = against_sales_order
        item["so_detail"] = so_detail
    if against_sales_invoice and si_detail:
        item["against_sales_invoice"] = against_sales_invoice
        item["si_detail"] = si_detail
    return item


def createDeliveryNote(customer_name, itemsDict, posting_date):

    posting_date = date_parse(posting_date)
    customer_name_pk = getOrCreateCustomer(customer_name)
    entryDoc = frappe.get_doc(
        {
            "doctype": "Delivery Note",
            "customer": customer_name_pk,
            "posting_date": posting_date,
            "docstatus": 1,
        }
    )
    for item in itemsDict:
        _ = entryDoc.append("items", {**item})
    entryDoc.insert()
    return entryDoc.name
