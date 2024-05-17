import frappe
import pandas as pd
from nr.nr_utils.auto_stock_entry_import import processAutoStockEntryImport
from nr.nr_utils.warehouse import getOrCreateWarehouse

# Column names
colsReqNoBlank = ["id", "posting_date", "item_inout", "item_code", "qty"]

colsReqNullable = ["from_warehouse", "to_warehouse"]

# colsOpt = ["basic_rate"]

colsReqAll = [*colsReqNoBlank, *colsReqNullable]


def processStockEntryGroup(dfg):

    group_key = dfg.iloc[0, :]["id"]
    print("----------- processing: ", group_key, " :----------------")

    # Make sure that there is no duplicated item since this will cuase problem with validation of payment entry and delivery note.
    filtItemDup = dfg["item_code"].duplicated()
    if filtItemDup.any():
        frappe.msgprint(f"Foun duplicate item {group_key}. Use the first occurrence")
        dfg = dfg[~filtItemDup]

    # Check whether these info are all duplicated.
    colsDup = ["id", "posting_date", "item_inout", "to_warehouse", "from_warehouse"]
    dfd = dfg[colsDup].copy()
    dfd = dfd.drop_duplicates()

    # If the dataframe does not have one row, this means the data is inconsistent.
    if dfd.shape[0] != 1:
        frappe.msgprint(
            msg=f"Found inconsistent data in [{group_key}]. Using values from the first row."
        )

    row = dfd.iloc[0, :]
    posting_date = row["posting_date"]
    item_inout = row["item_inout"]
    to_warehouse = row["to_warehouse"]
    from_warehouse = row["from_warehouse"]

    itemsArray = []
    for _, row in dfg.iterrows():
        item = dict(
            item_code=row["item_code"],
            qty=row["qty"],
        )
        if "basic_rate" in row:
            item["basic_rate"] = row["basic_rate"]
        itemsArray.append(item)

    processAutoStockEntryImport(
        itemsArray=itemsArray,
        posting_date=posting_date,
        item_inout=item_inout,
        to_warehouse=to_warehouse,
        from_warehouse=from_warehouse,
    )

    frappe.db.commit()


def processExcelWarehouse(row, key):
    warehouse_name = row[key]
    if warehouse_name:
        warehouse_name_pk = getOrCreateWarehouse(warehouse_name)
        return warehouse_name_pk
    return warehouse_name


def processExcelAutoStockEntryImport(filepath):
    dft = pd.read_excel(
        filepath,
        dtype={
            "id": str,
            "posting_date": str,
        },
    )
    cols = dft.columns.values

    for c in colsReqAll:
        if c not in cols:
            frappe.throw(title="Error", msg=f"Missing {c} column.")

    dft.apply(lambda row: processExcelWarehouse(row, "to_warehouse"), axis=1)
    dft.apply(lambda row: processExcelWarehouse(row, "from_warehouse"), axis=1)

    dft.groupby(by="id").apply(processStockEntryGroup)
