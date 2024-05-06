import frappe
import pandas as pd

# from nr.nr_utils.warehouse import getOrCreateWarehouse
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

    # Required
    # item_code = row["item_code"]
    # item_name = row["item_name"]
    #
    # Optional
    # uom_name = row["uom"]
    # warehouse_name = row["warehouse"]
    # item_group_name = row["item_group"]
    # valuation_rate = row["valuation_rate"]
    # opening_stock = row["opening_stock"]
    # allow_negative_stock = row["allow_negative_stock"]
    # parent_warehouse_name = row["parent_warehouse_name"]
    # must_be_whole_number = row["must_be_whole_number"]
    #
    # processAutoItemImport(
    #     item_name=item_name,
    #     item_code=item_code,
    #     opening_stock=opening_stock,
    #     warehouse_name=warehouse_name,
    #     must_be_whole_number=must_be_whole_number,
    #     allow_negative_stock=allow_negative_stock,
    #     valuation_rate=valuation_rate,
    #     item_group_name=item_group_name,
    #     uom_name=uom_name,
    #     parent_warehouse_name=parent_warehouse_name,
    # )

    idx = row["item_code"]

    itemData = dict()

    # Process required value
    for col in colsReq:
        value = row[col]
        if value:
            itemData[col] = value
        else:
            frappe.throw(msg=f"Require {col} in item: {idx}.")

    # Process optional values
    for col in colsAll:
        value = row[col]
        if value:
            itemData[col] = value

    processAutoItemImport(**itemData)

    frappe.db.commit()

    return None


# def processExcelWarehouse(row):
#     warehouse_name = row["warehouse"]
#     warehouse_name_pk = getOrCreateWarehouse(warehouse_name)
#     return warehouse_name_pk


def processExcelItemFile(filepath):

    # defaultItemGroup = "DEFAULT"
    # defaultValuationRate = 0.01
    # defaultWarehouse = "Store"
    #
    dft = pd.read_excel(filepath)
    cols = dft.columns.values

    for c in colsAll:
        if c not in cols:
            frappe.throw(title="Error", msg=f"Missing {c} column.")
    df = dft[colsAll]

    # # Handle optional columns
    # if "item_group" in cols:
    #     df["item_group"] = dft["item_group"].fillna(defaultItemGroup)
    # else:
    #     df["item_group"] = defaultItemGroup
    #
    # if "valuation_rate" in cols:
    #     df["valuation_rate"] = dft["valuation_rate"].fillna(defaultValuationRate)
    # else:
    #     df["valuation_rate"] = defaultValuationRate
    #
    # if "opening_stock" in cols:
    #     df["opening_stock"] = dft["opening_stock"].fillna(0)
    # else:
    #     df["opening_stock"] = 0
    #
    # if "warehouse" in cols:
    #     df["warehouse"] = dft["warehouse"].fillna(defaultWarehouse)
    # else:
    #     df["warehouse"] = defaultWarehouse
    #
    # if "uom" in cols:
    #     df["uom"] = dft["uom"].fillna("nos")
    # else:
    #     df["uom"] = "nos"

    # df.apply(processExcelWarehouse, axis=1)
    df.apply(processExcelItemRowFn, axis=1)
    return df
