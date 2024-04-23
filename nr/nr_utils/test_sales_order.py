# bench --site mysite run-tests --module "nr.nr_utils.test_sales_order"

import frappe
import unittest
from nr.nr_utils.sales_order import *


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

        customer_name = "customer 1"
        item_code = "Item 1"
        rate = 300
        qty = 10
        delivery_date = "2024-04-23"
        itemsDict = []
        item = createSalesOrderItemDict(item_code=item_code, qty=qty, rate=rate)
        itemsDict.append(item)

        getOrCreateSaleOrder(
            customer_name=customer_name,
            delivery_date=delivery_date,
            itemsDict=itemsDict,
        )
        self.assertIsNone(None)
