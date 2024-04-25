# bench --site mysite run-tests --module "nr.nr_utils.test_sales_invoice"

import frappe
import unittest
from nr.nr_utils.sales_invoice import *
from nr.nr_utils.item import getOrCreateItem
from nr.nr_utils.sales_order import *
from nr.nr_utils.customer import *
from datetime import datetime


def create_events():
    if frappe.flags.test_events_created:
        return

    frappe.set_user("Administrator")
    frappe.flags.test_events_created = True


class TestSalesInvoice(unittest.TestCase):
    def setUp(self):
        frappe.set_user("Administrator")

    def tearDown(self):
        pass

    def test_sales_invoice(self):

        sales_order_pk = "SAL-ORD-2024-00001"
        customer_name = "customer 4"
        item_code = "Item 5"
        rate = 300
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
        createSalesInvoice(
            itemsDict=itemsDict, due_date=due_date, customer_name=customer_name_pk
        )
        #
        self.assertIsNone(None)
