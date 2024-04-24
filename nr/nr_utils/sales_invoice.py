import frappe


def createSalesInvoiceItemDict():
    pass


def createSalesInvoice():

    itemsDict = [{}]

    entryDoc = frappe.get_doc(
        {
            "doctype": "Sales Invoice",
        }
    )
    for item in itemsDict:
        _ = entryDoc.append("items", {**item})
    entryDoc.insert()

    pass
