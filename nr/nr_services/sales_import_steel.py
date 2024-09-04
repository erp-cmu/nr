import frappe
import pandas as pd
import re
import numpy as np
from lxml import objectify
from datetime import timedelta
from nr.nr_utils.common import date_parse
from nr.nr_services.sales_import import processExcelAutoSalesFile

    
def processXMLSteel(filepath):

    def fmt(x):
        if isinstance(x, str):
            return x
        else:
            return ""

    def rowTypeTag(row):
        txt = row["เอกสารวันที่/รหัสสินค้า"]
        if not isinstance(txt, str):
            return "TOTAL"
        match = re.match(r"\d{4}-\d+-\d+", txt)  # Match always start from beginning.
        if match:
            return "SALE_ORDER"
        else:
            return "SALE_ORDER_ITEM"
    
    groupNo = {"value": 0}  # Make it mutable using ref datatype
    def groupTag(row):
        rowType = row["rowType"]
        if rowType == "SALE_ORDER":
            groupNo["value"] = groupNo["value"] + 1
        return groupNo["value"]
    
    def applyGroupFn(df):
        dateOnly = "%Y-%m-%d"
        filtRowType = df["rowType"] == "SALE_ORDER"
        saleOrder = df[filtRowType].iloc[0, :]
        filtSaleOrderItem = df["rowType"] == "SALE_ORDER_ITEM"
        dfOut = df[filtSaleOrderItem].copy()
        date = saleOrder["เอกสารวันที่/รหัสสินค้า"]
        time = saleOrder["เวลา/คลัง"]
        dt = date_parse(f"{date} {time}")
        dtStr = dt.strftime(dateOnly)
        dtBack = dt - timedelta(minutes=10)
        dtBackStr = dtBack.strftime(dateOnly)
        customer = saleOrder["ชื่อลูกหนี้/เจ้าหนี้/ราคา"]

        dfOut["custom_external_sales_order_id"] = saleOrder["เอกสารเลขที่/ชื่อสินค้า"]
        dfOut["posting_date"] = dtBackStr
        dfOut["due_date"] = dtStr
        dfOut["delivery_date"] = dtStr
        dfOut["customer_name"] = customer
        return dfOut

    xml_data = objectify.parse(filepath)  # Parse XML data
    root = xml_data.getroot()  # Root element
    table = root.Worksheet.Table  # Table
    maxCol = np.array([c1.countchildren() for c1 in table.getchildren()]).max()
    data = []
    for c1 in table.getchildren():
        if c1.countchildren() > 5:
            rowData = [np.nan for i in range(maxCol)]
            for idx, c2 in enumerate(c1.getchildren()):
                # print(c2.countchildren())
                if c2.countchildren() > 1:
                    raise Exception("Expect 1 child here")
                cellData = c2.getchildren()[0]
                if not isinstance(cellData, objectify.StringElement) and not isinstance(
                    cellData, objectify.FloatElement
                ):
                    raise Exception("Expect cell to be StringElement")
                # print(cellData)
                if cellData.text:  # can be NoneType
                    rowData[idx] = cellData.text

            data.append(rowData)
    colsOri = []
    cols1 = data[0]
    cols2 = data[1]
    for col1, col2 in zip(cols1, cols2):
        col1str = fmt(col1)
        col2str = fmt(col2)
        if col2str:
            colsOri.append(f"{col1str}/{col2str}")
        else:
            colsOri.append(col1str)
    dft1 = pd.DataFrame(data=data[2:], columns=colsOri)
    # Drop "empty" row
    dft1 = dft1.dropna(axis=0, how="all")
    # Drop row with "grand total"
    filt = dft1["เอกสารวันที่/รหัสสินค้า"].str.contains("Grand Total").astype(bool)
    dft1 = dft1[~filt]
    dft1["rowType"] = dft1.apply(rowTypeTag, axis=1)
    
    dft1["groupNo"] = dft1.apply(groupTag, axis=1)
    dfG = dft1.groupby(by="groupNo")
    dft3 = dfG.apply(applyGroupFn)
    dft3 = dft3.reset_index(drop=True)
    dft3["custom_sales_order_source"] = "OTHER"
    dft3["item_code"] = dft3["เอกสารวันที่/รหัสสินค้า"]
    dft3["item_name"] = dft3["เอกสารเลขที่/ชื่อสินค้า"]
    dft3["rate"] = dft3["ชื่อลูกหนี้/เจ้าหนี้/ราคา"]
    dft3["qty"] = dft3["ลูกหนี้/เจ้าหนี้/จำนวน"]
    dft3["warehouse"] = dft3["เวลา/คลัง"]

    dft3["rate"] = dft3["rate"].str.replace(',', '').astype(float).fillna(0)
    dft3["qty"] = dft3["qty"].str.replace(',', '').astype(float).fillna(0)

    filtZeroQty = dft3["qty"] != 0
    dft3 = dft3[filtZeroQty]
    
    cols = ['เอกสารวันที่/รหัสสินค้า', 'เอกสารเลขที่/ชื่อสินค้า', 'เวลา/คลัง', 'เอกสารอ้างอิง/พื้นที่เก็บ', 'เอกสารอ้างอิงวันที่/หน่วยนับ', 'ลูกหนี้/เจ้าหนี้/จำนวน', 'ชื่อลูกหนี้/เจ้าหนี้/ราคา', 'มูลค่าสินค้า/ส่วนลด', 'มูลค่าส่วนลด/มูลค่าส่วนลด', 'มูลค่าหลังหักส่วนลด/รวมมูลค่า', 'มูลค่ายกเว้นภาษี', 'ภาษีมูลค่าเพิ่ม', 'มูลค่าสุทธิ', 'Cashier', 'rowType', 'groupNo', 'custom_external_sales_order_id', 'custom_sales_order_source', 'posting_date', 'due_date', 'delivery_date', 'customer_name', 'item_code', 'item_name', 'rate', 'qty', 'warehouse']
    dft3 = dft3[cols]
    
    filename = "/private/files/steel_sales_temp.xlsx"
    filepath = frappe.get_site_path() + filename
    dft3.to_excel(filepath, index=False)
    processExcelAutoSalesFile(filepath=filepath)
