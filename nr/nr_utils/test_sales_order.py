# bench --site mysite run-tests --module "nr.nr_utils.test_sales_order"

import frappe
import unittest
from nr.nr_utils.item import getOrCreateItem
from nr.nr_utils.sales_order import *
from nr.nr_utils.customer import *
from datetime import datetime


def create_events():
    if frappe.flags.test_events_created:
        return

    frappe.set_user("Administrator")
    frappe.flags.test_events_created = True


class TestSalesOrder(unittest.TestCase):
    def setUp(self):
        frappe.set_user("Administrator")

    def tearDown(self):
        pass

    def test_sales_order(self):

        # Input
        customer_name = "Customer 2"
        itemsArray = [
            dict(item_code="ITEM001", item_name="Item 1", rate=300, qty=10),
            dict(item_code="ITEM002", item_name="Item 2", rate=200, qty=20),
        ]
        now = datetime.now()
        delivery_date = now.strftime("%Y-%m-%d")

        # Logic
        customer_name_pk = getOrCreateCustomer(customer_name=customer_name)
        itemsDict = []
        for itemsArrayEle in itemsArray:
            item_code = itemsArrayEle["item_code"]
            item_name = itemsArrayEle["item_name"]
            rate = itemsArrayEle["rate"]
            qty = itemsArrayEle["qty"]
            item_code_pk = getOrCreateItem(
                item_code=item_code, item_name=item_name, allow_negative_stock=True
            )
            item = createSalesOrderItemDict(item_code=item_code_pk, qty=qty, rate=rate)
            itemsDict.append(item)

        sales_order_pk = createSalesOrder(
            customer_name=customer_name_pk,
            delivery_date=delivery_date,
            itemsDict=itemsDict,
        )
        print(sales_order_pk)
        self.assertIsNone(None)
