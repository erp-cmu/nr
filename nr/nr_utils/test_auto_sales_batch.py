# bench --site mysite run-tests --module "nr.nr_utils.test_auto_sales_batch"

import frappe
import unittest
from nr.nr_utils.auto_sales import *
from datetime import datetime


def create_events():
    if frappe.flags.test_events_created:
        return

    frappe.set_user("Administrator")
    frappe.flags.test_events_created = True


class TestAutoSalesBatch(unittest.TestCase):
    def setUp(self):
        frappe.set_user("Administrator")

    def tearDown(self):
        pass

    def test_auto_sales_batch(self):
        # Input
        customer_name = "Customer 3"
        # NOTE: I include options for valuation rate here.
        itemsArray = [
            dict(
                item_code="ITEM005",
                item_name="Item 5",
                rate=300,
                qty=10,
                # valuation_rate=300,
            ),
            dict(
                item_code="ITEM006",
                item_name="Item 6",
                rate=200,
                qty=20,
                # valuation_rate=200,
            ),
        ]
        now = datetime.now()
        delivery_date = now.strftime("%Y-%m-%d")
        due_date = now.strftime("%Y-%m-%d")
        posting_date = now.strftime("%Y-%m-%d")
        processAutoSale(
            customer_name=customer_name,
            itemsArray=itemsArray,
            delivery_date=delivery_date,
            due_date=due_date,
            posting_date=posting_date,
        )
