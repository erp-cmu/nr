import frappe
import pandas as pd


def getOrCreateUOM(uom_name, must_be_whole_number=False):

    if frappe.db.exists("UOM", uom_name):
        return uom_name

    doc = frappe.get_doc(
        {
            "doctype": "UOM",
            "uom_name": uom_name,
            "must_be_whole_number": must_be_whole_number,
        }
    )
    doc.insert()
    return doc.name


def getOrCreateItemGroup(
    item_group_name, parent_item_group="All Item Groups", is_group=False
):

    item_group_name_pk = frappe.db.exists("Item Group", item_group_name)
    if item_group_name_pk:
        return item_group_name_pk

    doc = frappe.get_doc(
        {
            "doctype": "Item Group",
            "item_group_name": item_group_name,
            "parent_item_group": parent_item_group,
            "is_group": is_group,
        }
    )
    doc.insert()
    return doc.name


def getOrCreateItem(
    item_code,
    item_name,
    item_group="Products",
    stock_uom="Nos",
    opening_stock=0,
    valuation_rate=0.01,  # NOTE: I put non-zero number here so that the software can calculate valuation and does not complain when performing stock entry.
    allow_negative_stock=False,
    is_stock_item=True,
):

    item_name_pk = frappe.db.exists("Item", {"item_code": item_code})
    if item_name_pk:
        return item_name_pk

    item_name_pk = frappe.db.exists("Item", {"item_name": item_name})
    if item_name_pk:
        return item_name_pk

    doc = frappe.get_doc(
        {
            "doctype": "Item",
            "item_code": item_code,
            "item_name": item_name,
            "item_group": item_group,
            "stock_uom": stock_uom,
            "opening_stock": opening_stock,
            "valuation_rate": valuation_rate,
            "allow_negative_stock": allow_negative_stock,
            "is_stock_item": is_stock_item,
        },
    )
    doc.insert()
    return doc.name
