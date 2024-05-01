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

    return entryDoc.name


def getSalesInvoiceItem(sales_invoice_name, item_code):

    sales_invoice_name_pk = frappe.db.exists(
        "Sales Invoice", {"name": sales_invoice_name}
    )
    if not sales_invoice_name_pk:
        frappe.throw(msg="Cannot find sales invoice.")

    sales_invoice_item_name_pk = frappe.db.exists(
        "Sales Invoice Item", {"parent": sales_invoice_name_pk, "item_code": item_code}
    )
    if sales_invoice_item_name_pk:
        return sales_invoice_item_name_pk

    sales_invoice_item_name_pk = frappe.db.exists(
        "Sales Invoice Item", {"parent": sales_invoice_name_pk, "item_name": item_code}
    )
    if sales_invoice_item_name_pk:
        return sales_invoice_item_name_pk

    if not sales_invoice_item_name_pk:
        frappe.throw(msg="Cannot find sales invoice item.")

    return None
