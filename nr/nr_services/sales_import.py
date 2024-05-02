import frappe
import pandas as pd


def processExcelItemFile(filepath):
    dft = pd.read_excel(filepath)
    cols = dft.columns.values

    # Check requred columns
    colsReg = ["item_code", "item_name"]
    for c in colsReg:
        if c not in cols:
            frappe.throw(title="Error", msg=f"Missing {c} column.")
    df = dft[colsReg]
