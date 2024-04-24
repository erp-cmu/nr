import frappe


def createSalesInvoiceItemDict(item_code, qty, rate):

    item = dict(item_code=item_code, qty=qty, uom="Nos", rate=rate)
    return item



def createSalesInvoice(itemsDict):

    entryDoc = frappe.get_doc(
        {
            "doctype": "Sales Invoice",
        }
    )
    for item in itemsDict:
        _ = entryDoc.append("items", {**item})
    entryDoc.insert()

    pass
