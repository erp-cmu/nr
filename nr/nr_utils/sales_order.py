import frappe
from nr.nr_utils.customer import getOrCreateCustomer
from nr.nr_utils.common import date_parse
from datetime import datetime


def createSalesOrderItemDict(item_code, qty, rate):

    item = dict(item_code=item_code, qty=qty, uom="Nos", rate=rate)

    return item


def createSalesOrder(customer_name, delivery_date, itemsDict):

    customer_name_pk = getOrCreateCustomer(customer_name)

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
            "docstatus": 1,
        }
    )
    for item in itemsDict:
        _ = entryDoc.append("items", {**item})
    entryDoc.insert()
    return entryDoc.name


def updateSalesOrderStatus(sales_order_name, is_billed, is_delivered):

    sales_order_name_pk = frappe.db.exists("Sales Order", {"name": sales_order_name})
    if not sales_order_name_pk:
        frappe.throw(msg="Cannot find sales order.")

    # Retrieve current status
    curSO = frappe.db.get_value("Sales Order", sales_order_name_pk, ["*"], as_dict=True)
    status = curSO["status"]
    billing_status = curSO["billing_status"]
    delivery_status = curSO["delivery_status"]
    per_billed = curSO["per_billed"]
    per_delivered = curSO["per_delivered"]

    # Takes care of billing and delivery status
    if is_billed:
        billing_status = "Fully Billed"
        per_billed = 100
    if is_delivered:
        delivery_status = "Fully Delivered"
        per_delivered = 100

    # Takes care of status
    if is_billed and is_delivered:
        status = "Completed"
    elif is_billed and not is_delivered:
        status = "To Deliver"

    elif not is_billed and is_delivered:
        status = "To Bill"
    else:
        status = "To Deliver and Bill"

    # Update values
    frappe.db.set_value(
        "Sales Order",
        sales_order_name_pk,
        {
            "status": status,
            "billing_status": billing_status,
            "delivery_status": delivery_status,
            "per_billed": per_billed,
            "per_delivered": per_delivered,
        },
    )

    return sales_order_name_pk
