import frappe
import pandas as pd

from nr.nr_utils.warehouse import getOrCreateWarehouse
from nr.nr_utils.auto_item_import import processAutoItemImport


# Column names
colsReqNoBlank = [
    "item_code",
    "item_name",
]

colsReqNullable = [
    "opening_stock",
    "warehouse_name",
    "allow_negative_stock",
    "valuation_rate",
    "must_be_whole_number",
    "item_group_name",
    "uom_name",
]

colsOpt = ["parent_warehouse_name", "is_stock_item"]


colsReqAll = [*colsReqNoBlank, *colsReqNullable]


def processExcelItemRowFn(row):

    item_code_idx = row["item_code"]

    print("----------- processing: ", item_code_idx, " :----------------")
    itemData = dict()

    # Process required columns with non-blank value
    for col in colsReqNoBlank:
        value = row[col]
        if value:
            itemData[col] = value
        else:
            frappe.throw(msg=f"Require {col} in item: {item_code_idx}.")

    # Process required column with nullable values
    for col in colsReqAll:
        value = row[col]
        if value:
            itemData[col] = value

    # Process optional columns
    for col in colsOpt:
        if col in row.index:
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

    for c in colsReqAll:
        if c not in cols:
            frappe.throw(title="Error", msg=f"Missing {c} column.")
    df = dft[colsReqAll]

    # NOTE: I need to create warehouse before create item.
    # Without this method, I encountered error about warehouse not connected to account
    # if there is more than one new warehouse to create.  This behavior was not observed
    # when running the test.  I think this might have something to do with caching of variables.
    # The problem is this "warehouse_account" variable that appears in "if warehouse_account.get(sle.warehouse):" in stock_controller.py

    df.apply(processExcelWarehouse, axis=1)
    df.apply(processExcelItemRowFn, axis=1)
    return df
