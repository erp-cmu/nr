import frappe
from nr.nr_utils.customer import getOrCreateCustomer
from nr.nr_utils.common import date_parse
from datetime import datetime


def checkCustomExternalSalesOrderID(id):
    name = frappe.db.exists("Sales Order", {"custom_external_sales_order_id": id})

    if name:
        return name
    else:
        return None


def createSalesOrderItemDict(item_code, qty, rate):

    item = dict(item_code=item_code, qty=qty, uom="Nos", rate=rate)

    return item


def validateCustomSalesOrderSource(src):
    if src not in ["OTHER", "INTERNAL", "LAZADA", "LINE_SHOP", "SHOPEE"]:
        frappe.throw("Invalid custom sales order source")


def createSalesOrder(
    customer_name,
    delivery_date,
    itemsDict,
    custom_external_sales_order_id,
    custom_sales_order_source="OTHER",
):

    customer_name_pk = getOrCreateCustomer(customer_name)

    validateCustomSalesOrderSource(src=custom_sales_order_source)

    # Make sure that user input unique custom_external_sales_order_id
    if custom_sales_order_source != "INTERNAL":

        if not custom_external_sales_order_id:
            frappe.throw(msg="Custom external sales order ID is required.")

        so = checkCustomExternalSalesOrderID(id=custom_external_sales_order_id)
        if so:
            frappe.throw(msg="Duplicated custom external sales order ID")

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
            "custom_external_sales_order_id": custom_external_sales_order_id,
            "custom_sales_order_source": custom_sales_order_source,
            "docstatus": 1,
        }
    )
    for item in itemsDict:
        _ = entryDoc.append("items", {**item})
    entryDoc.insert()
    return entryDoc.name


def getSalesOrderItem(sales_order_name, item_code):

    sales_order_name_pk = frappe.db.exists("Sales Order", {"name": sales_order_name})
    if not sales_order_name_pk:
        frappe.throw(msg="Cannot find sales order.")

    sales_order_item_name_pk = frappe.db.exists(
        "Sales Order Item", {"parent": sales_order_name_pk, "item_code": item_code}
    )
    if sales_order_item_name_pk:
        return sales_order_item_name_pk

    sales_order_item_name_pk = frappe.db.exists(
        "Sales Order Item", {"parent": sales_order_name_pk, "item_name": item_code}
    )
    if sales_order_item_name_pk:
        return sales_order_item_name_pk

    if not sales_order_item_name_pk:
        frappe.throw(msg="Cannot find sales order item.")

    return None


def updateSalesOrderStatus(sales_order_name, is_billed, is_delivered):

    sales_order_name_pk = frappe.db.exists("Sales Order", {"name": sales_order_name})
    if not sales_order_name_pk:
        frappe.throw(msg="Cannot find sales order.")

    # NOTE: For some reason, the initial values are not correct, so I am going to specify all the values myself and not rely on the current values.
    # Retrieve current status
    # curSO = frappe.db.get_value("Sales Order", sales_order_name_pk, ["*"], as_dict=True)
    # status = curSO["status"]
    # billing_status = curSO["billing_status"]
    # delivery_status = curSO["delivery_status"]
    # per_billed = curSO["per_billed"]
    # per_delivered = curSO["per_delivered"]

    # Takes care of billing and delivery status
    if is_billed:
        billing_status = "Fully Billed"
        per_billed = 100
    else:
        billing_status = "Not Billed"
        per_billed = 0

    if is_delivered:
        delivery_status = "Fully Delivered"
        per_delivered = 100
    else:
        delivery_status = "Not Delivered"
        per_delivered = 0

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
