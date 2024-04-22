import frappe
import unittest
from nr.nr_utils.item import createOrGetItem, createUOM, createOrGetItemGroup
from nr.nr_utils.warehouse import getOrCreateWarehouse
from nr.nr_utils.stock_entry import createStockEntry, createStockEntryItemDict
from nr.nr_utils.sales_order import a
def create_events():
    if frappe.flags.test_events_created:
        return

    frappe.set_user("Administrator")
    frappe.flags.test_events_created = True


class TestEvent(unittest.TestCase):
    def setUp(self):
        frappe.set_user("Administrator")

    def tearDown(self):
        pass

    def test_sales_order(self):

 
        self.assertIsNone(None)
