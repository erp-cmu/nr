import frappe
import pandas as pd
from nr.nr_utils.auto_sales import processAutoSale


def processSalesOrderGroup(dfg):

    group_key = dfg.iloc[0, :]["custom_external_sales_order_id"]
    print("----------- processing: ", group_key, " :----------------")

    # Make sure that there is no duplicated item since this will cuase problem with validation of payment entry and delivery note.
    filtItemDup = dfg["item_code"].duplicated()
    if filtItemDup.any():
        frappe.msgprint(f"Foun duplicate item {group_key}. Use the first occurrence")
        dfg = dfg[~filtItemDup]

    # Check whether these info are all duplicated.
    colsDup = [
        "custom_external_sales_order_id",
        "custom_sales_order_source",
        "posting_date",
        "due_date",
        "delivery_date",
        "customer_name",
    ]
    dfd = dfg[colsDup].copy()
    dfd = dfd.drop_duplicates()

    # If the dataframe does not have one row, this means the data is inconsistent.
    if dfd.shape[0] != 1:
        frappe.msgprint(
            msg=f"Found inconsistent data in [{group_key}]. Using values from the first row."
        )

    row = dfd.iloc[0, :]
    customer_name = row["customer_name"]
    delivery_date = row["delivery_date"]
    due_date = row["due_date"]
    posting_date = row["posting_date"]
    custom_external_sales_order_id = row["custom_external_sales_order_id"]
    custom_sales_order_source = row["custom_sales_order_source"]

    itemsArray = []
    for idx, row in dfg.iterrows():
        item = dict(
            item_code=row["item_code"],
            item_name=row["item_name"],
            rate=row["rate"],
            qty=row["qty"],
        )
        itemsArray.append(item)

    processAutoSale(
        customer_name=customer_name,
        itemsArray=itemsArray,
        delivery_date=delivery_date,
        due_date=due_date,
        posting_date=posting_date,
        custom_external_sales_order_id=custom_external_sales_order_id,
        custom_sales_order_source=custom_sales_order_source,
        stock_uom="Nos_frac",
    )

    frappe.db.commit()


def processExcelAutoSalesFile(filepath):
    dft = pd.read_excel(
        filepath,
        dtype={
            "custom_external_sales_order_id": str,
            "posting_date": "str",
            "due_date": "str",
            "delivery_date": "str",
        },
    )
    cols = dft.columns.values

    # Check requred columns
    colsReq = [
        "custom_external_sales_order_id",
        "custom_sales_order_source",
        "posting_date",
        "due_date",
        "delivery_date",
        "customer_name",
        "item_code",
        "item_name",
        "rate",
        "qty",
    ]
    for c in colsReq:
        if c not in cols:
            frappe.throw(title="Error", msg=f"Missing {c} column.")

    # Make sure customer name is clean
    dft["customer_name"] = dft["customer_name"].str.strip().str.replace("  ", " ")

    dft["custom_sales_order_source"] = dft["custom_sales_order_source"].fillna("OTHER")

    dft.groupby(by="custom_external_sales_order_id").apply(processSalesOrderGroup)
