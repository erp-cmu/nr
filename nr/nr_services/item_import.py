import frappe
import pandas as pd

from nr.nr_utils.warehouse import getOrCreateWarehouse
from nr.nr_utils.item import getOrCreateItem, getOrCreateItemGroup, getOrCreateUOM
from nr.nr_utils.stock_entry import createStockEntryItemDict, createStockEntry


def processExcelItemRowFn(row):
    item_group_name = row["item_group"]
    item_group_name_pk = getOrCreateItemGroup(item_group_name=item_group_name)

    uom_name = row["uom"]
    uom_name_pk = getOrCreateUOM(uom_name=uom_name)

    warehouse_name = row["warehouse"]
    warehouse_name_pk = getOrCreateWarehouse(warehouse_name)
    item_code = row["item_code"]
    item_name = row["item_name"]

    item_code_temp = getOrCreateItem(
        item_code=item_code,
        item_name=item_name,
        item_group=item_group_name_pk,
        stock_uom=uom_name_pk,
        opening_stock=0,
    )

    qty = row["opening_stock"]
    if qty > 0:
        itemDict = createStockEntryItemDict(
            item_code=item_code,
            qty=qty,
        )
        itemsDict = [itemDict]
        createStockEntry(
            itemsDict=itemsDict, to_warehouse=warehouse_name_pk, item_inout="IN"
        )
    return None


def processExcelWarehouse(row):
    warehouse_name = row["warehouse"]
    warehouse_name_pk = getOrCreateWarehouse(warehouse_name)
    return warehouse_name_pk


def processExcelItemFile(filepath):

    defaultItemGroup = "DEFAULT"
    defaultValuationRate = 0.01
    defaultWarehouse = "Store"

    dft = pd.read_excel(filepath)
    cols = dft.columns.values

    # Check requred columns
    colsReq = ["item_code", "item_name"]
    for c in colsReq:
        if c not in cols:
            frappe.throw(title="Error", msg=f"Missing {c} column.")
    df = dft[colsReq]

    # Handle optional columns
    if "item_group" in cols:
        df["item_group"] = dft["item_group"].fillna(defaultItemGroup)
    else:
        df["item_group"] = defaultItemGroup

    if "valuation_rate" in cols:
        df["valuation_rate"] = dft["valuation_rate"].fillna(defaultValuationRate)
    else:
        df["valuation_rate"] = defaultValuationRate

    if "opening_stock" in cols:
        df["opening_stock"] = dft["opening_stock"].fillna(0)
    else:
        df["opening_stock"] = 0

    if "warehouse" in cols:
        df["warehouse"] = dft["warehouse"].fillna(defaultWarehouse)
    else:
        df["warehouse"] = defaultWarehouse

    if "uom" in cols:
        df["uom"] = dft["uom"].fillna("nos")
    else:
        df["uom"] = "nos"

    df.apply(processExcelWarehouse, axis=1)
    df.apply(processExcelItemRowFn, axis=1)
    return df
