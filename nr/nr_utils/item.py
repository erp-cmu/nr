import frappe


def getFirstCompany():
    res = frappe.get_all("Company")
    return res[0]["name"]


def createUOM(uom_name, must_be_whole_number=False):

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


def createWarehouse(
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


def createItemGroup(
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


def createItem(
    item_code,
    item_name,
    item_group,
    stock_uom,
    opening_stock=0,
    valuation_rate=0.01,
    allow_negative_stock=False,
    is_stock_item=True,
):

    item_name_pk = frappe.db.exists("Item", {"item_code", item_code})
    if item_name_pk:
        return item_name_pk

    item_name_pk = frappe.db.exists("Item", {"item_name", item_name})
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
