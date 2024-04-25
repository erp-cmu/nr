import frappe
from nr.nr_utils.customer import getOrCreateCustomer
from nr.nr_utils.account import getAccountPK


def createPaymentReferencesItemDict(reference_name):

    item = dict(reference_name=reference_name)
    return item


def createPaymentEntryReceive(customer_name, received_amount, itemsDict):

    payment_type = "Receive"
    # if (payment_type != "Receive") or ( payment_type != "Pay" ) or payment_type != ("Internal Transfer"):
    #     frappe.throw(msg="Please use correct value for payment_type")

    party_type = "Customer"
    # if (party_type != "Customer") or (party_type != "Supplier"):
    #     frappe.throw(msg="Please use correct value for payment_type")

    account_paid_to_pk = getAccountPK(name="Bank Account")
    # This field is optional but I am using it just to remind myself.
    account_paid_from_pk = getAccountPK(name="Debtors")

    if (not account_paid_to_pk) or (not account_paid_from_pk):
        frappe.throw(msg=f"Cannot find accounts: Bank Account and/or Debtors.")

    customer_name_pk = getOrCreateCustomer(customer_name)

    paid_amount = received_amount

    # Constructing doc
    entryDoc = frappe.get_doc(
        {
            "doctype": "Payment Entry",
            "payment_type": payment_type,
            "party": customer_name_pk,
            "party_type": party_type,
            # "party_name": customer_name_pk,
            "paid_amount": paid_amount,
            "received_amount": received_amount,
            "target_exchange_rate": 1,
            "paid_to_account_currency": "THB",
            "paid_to": account_paid_to_pk,
            "paid_from": account_paid_from_pk,
            "reference_no": "REFERENCE_NO",
            "reference_date": "2024-04-25",
            "docstatus": 1,
        }
    )

    for item in itemsDict:
        _ = entryDoc.append("items", {**item})

    entryDoc.insert()

    return entryDoc.name
