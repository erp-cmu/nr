import frappe


def getFirstCompany():
    res = frappe.get_all("Company")
    return res[0]["name"]
