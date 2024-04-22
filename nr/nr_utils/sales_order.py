import frappe
from nr.nr_utils.customer import getOrCreateCustomer
from nr.nr_utils.common import date_parse
from datetime import datetime


def createSalesOrderItemDict(item_code, qty):

    item = dict(item_code=item_code, qty=qty, uom="Nos")

    return item


def getOrCreateSaleOrder(customer_name, delivery_date, itemsDict):

    customer_name_pk = getOrCreateCustomer(customer_name)
    print(customer_name_pk)

    if (type(delivery_date) is not datetime) and (type(delivery_date) is not str):
        frappe.throw("Please use datetime or string for time.")

    if type(delivery_date) is str:
        try:
            delivery_date = date_parse(delivery_date)
        except:
            frappe.throw("Cannot parse date string.")

    entryDoc = frappe.get_doc(
        {
            "doctype": "Sales Order",
            "customer": customer_name_pk,
            "delivery_date": delivery_date,
        }
    )
    for item in itemsDict:
        _ = entryDoc.append("items", {**item})
    entryDoc.insert()
    pass
