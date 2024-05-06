import frappe
import pandas as pd

from nr.nr_utils.warehouse import getOrCreateWarehouse
from nr.nr_utils.auto_item_import import processAutoItemImport


# Column names
colsReq = [
    "item_code",
    "item_name",
]

colsOpt = [
    "opening_stock",
    "warehouse_name",
    "allow_negative_stock",
    "valuation_rate",
    "must_be_whole_number",
    "item_group_name",
    "uom_name",
    "parent_warehouse_name",
]

colsAll = [*colsReq, *colsOpt]


def processExcelItemRowFn(row):

    item_code_idx = row["item_code"]

    print("----------- processing: ", item_code_idx, " :----------------")
    itemData = dict()

    # Process required value
    for col in colsReq:
        value = row[col]
        if value:
            itemData[col] = value
        else:
            frappe.throw(msg=f"Require {col} in item: {item_code_idx}.")

    # Process optional values
    for col in colsAll:
        value = row[col]
        if value:
            itemData[col] = value

    processAutoItemImport(**itemData)

    frappe.db.commit()

    return None


def processExcelWarehouse(row):
    warehouse_name = row["warehouse_name"]
    if warehouse_name:
        warehouse_name_pk = getOrCreateWarehouse(warehouse_name)
        return warehouse_name_pk
    return warehouse_name


def processExcelItemFile(filepath):

    dft = pd.read_excel(filepath)
    cols = dft.columns.values

    for c in colsAll:
        if c not in cols:
            frappe.throw(title="Error", msg=f"Missing {c} column.")
    df = dft[colsAll]

    # NOTE: I need to create warehouse before create item.
    # Without this method, I encountered error about warehouse not connected to account
    # if there is more than one new warehouse to create.  This behavior was not observed
    # when running the test.  I think this might have something to do with caching of variables.
    # The problem is this "warehouse_account" variable that appears in "if warehouse_account.get(sle.warehouse):" in stock_controller.py

    df.apply(processExcelWarehouse, axis=1)
    df.apply(processExcelItemRowFn, axis=1)
    return df
