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
        itemsArray = [
            dict(
                item_code="ITEM005",
                item_name="Item 5",
                rate=300,
                qty=0.15,
            ),
            dict(
                item_code="ITEM006",
                item_name="Item 6",
                rate=200,
                qty=0.23,
            ),
        ]
        now = datetime.now()
        dtNow = now.strftime("%Y-%m-%d")
        delivery_date = dtNow
        due_date = dtNow
        posting_date = dtNow

        for id in ["ID4", "ID5", "ID6"]:
            processAutoSale(
                customer_name=customer_name,
                itemsArray=itemsArray,
                delivery_date=delivery_date,
                due_date=due_date,
                posting_date=posting_date,
                custom_external_sales_order_id=id,
                stock_uom="Nos_frac",
            )
