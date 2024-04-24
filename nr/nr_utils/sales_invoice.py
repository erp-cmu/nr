import frappe
from datetime import datetime
from nr.nr_utils.common import date_parse
from nr.nr_utils.customer import getOrCreateCustomer


def createSalesInvoiceItemDict(item_code, qty, rate, sales_order):

    item = dict(
        item_code=item_code, qty=qty, uom="Nos", rate=rate, sales_order=sales_order
    )
    return item


def createSalesInvoice(itemsDict, due_date, customer_name):

    customer_name_pk = getOrCreateCustomer(customer_name)

    if (type(due_date) is not datetime) and (type(due_date) is not str):
        frappe.throw("Please use datetime or string for time.")

    if type(due_date) is str:
        try:
            due_date = date_parse(due_date)
        except:
            frappe.throw("Cannot parse date string.")

    entryDoc = frappe.get_doc(
        {
            "doctype": "Sales Invoice",
            "due_date": due_date,
            "customer": customer_name_pk,
            "docstatus": 1,
        }
    )
    for item in itemsDict:
        _ = entryDoc.append("items", {**item})
    #
    entryDoc.insert()

    pass
