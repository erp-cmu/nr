# bench --site mysite run-tests --module "nr.nr_utils.test_payment_entry"

import frappe
import unittest
from nr.nr_utils.sales_invoice import *
from nr.nr_utils.item import getOrCreateItem
from nr.nr_utils.sales_order import *
from nr.nr_utils.customer import *
from datetime import datetime
from nr.nr_utils.payment_entry import *


def create_events():
    if frappe.flags.test_events_created:
        return

    frappe.set_user("Administrator")
    frappe.flags.test_events_created = True


class TestPaymentEntry(unittest.TestCase):
    def setUp(self):
        frappe.set_user("Administrator")

    def tearDown(self):
        pass

    def test_payment_entry(self):
        customer_name = "customer 6"
        item_code = "Item 6"
        rate = 1000
        qty = 10
        now = datetime.now()
        due_date = now.strftime("%Y-%m-%d")
        delivery_date = due_date
        customer_name_pk = getOrCreateCustomer(customer_name=customer_name)
        item_code_pk = getOrCreateItem(item_code=item_code, item_name=item_code)

        # Create sales order
        itemsDict = []
        item = createSalesOrderItemDict(item_code=item_code_pk, qty=qty, rate=rate)
        itemsDict.append(item)
        sales_order_pk = createSalesOrder(
            customer_name=customer_name_pk,
            delivery_date=delivery_date,
            itemsDict=itemsDict,
        )

        # Create sales invoice
        itemsDict = []
        item = createSalesInvoiceItemDict(
            item_code=item_code_pk, qty=qty, rate=rate, sales_order=sales_order_pk
        )
        itemsDict.append(item)
        #
        sales_invoice_pk = createSalesInvoice(
            itemsDict=itemsDict, due_date=due_date, customer_name=customer_name_pk
        )
        total_amount = rate * qty
        itemsDict = []
        item = createPaymentReferencesItemDict(reference_name=sales_invoice_pk, total_amount=total_amount, allocated_amount=total_amount)
        itemsDict.append(item)
        createPaymentEntryReceive(customer_name=customer_name_pk, received_amount=total_amount, itemsDict=itemsDict)
        pass
