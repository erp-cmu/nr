import frappe
from nr.nr_utils.company import getFirstCompany

def getAccountPK(name, company=None):
    if not company:
        company = getFirstCompany()

    account_name_pk = None

    # Check primary key
    account_name_pk = frappe.db.exists("Account", name)
    if account_name_pk:
        return account_name_pk

    # Check primary key with company name
    account_name_pk = frappe.db.exists("Account", f"{name} - {company}")
    if account_name_pk:
        return account_name_pk

    # Check account_name field
    account_name_pk = frappe.db.exists(
        {"doctype": "Account", "account_name": name}
    )
    if account_name_pk:
        return account_name_pk

    return account_name_pk



