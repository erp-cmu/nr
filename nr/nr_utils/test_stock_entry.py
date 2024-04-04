import frappe
import unittest
from nr.nr_utils.stock_entry import createStockEntry, createStockEntryItemDict


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

    # def test_stock_entry(self):
        # qty = 101
        # item_code = "I001"
        # itemDict = createStockEntryItemDict(
        #     item_code=item_code,
        #     qty=qty,
        # )
        # itemsDict = [itemDict]
        #
        # to_warehouse = "CCC - IE"
        #
        # createStockEntry(
        #     itemsDict=itemsDict, to_warehouse=to_warehouse, item_inout="IN"
        # )
        # self.assertIsNone(None)
