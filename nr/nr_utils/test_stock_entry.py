# bench --site mysite run-tests --module "nr.nr_utils.test_stock_entry"

import frappe
import unittest
from nr.nr_utils.stock_entry import createStockEntry, createStockEntryItemDict
from nr.nr_utils.item import getOrCreateItem
from nr.nr_utils.warehouse import getOrCreateWarehouse


def create_events():
    if frappe.flags.test_events_created:
        return

    frappe.set_user("Administrator")
    frappe.flags.test_events_created = True


class TestStockEntry(unittest.TestCase):
    def setUp(self):
        frappe.set_user("Administrator")

    def tearDown(self):
        pass

    def test_stock_entry(self):

        to_warehouse = "XXX1"
        from_warehouse = "XXX2"
        item_inout = "IN"
        item_inout = "OUT"
        item_inout = "TRANSFER"
        itemsArray = [
            dict(item_code="A0003", qty=10.5, basic_rate=100),
            dict(item_code="A0004", qty=100.5, basic_rate=200),
        ]
        posting_date = "2024-04-01"

        to_warehouse_pk = getOrCreateWarehouse(
            to_warehouse,
        )

        from_warehouse_pk = getOrCreateWarehouse(from_warehouse)

        itemsDict = []
        for item in itemsArray:
            item_code = item["item_code"]
            item_name = item_code
            if item_name in item:
                item_name = item["item_name"]
            stock_uom = "Nos_frac"
            if "uom" in item:
                stock_uom = item["uom"]
            basic_rate = 0.01
            if "basic_rate" in item:
                basic_rate = item["basic_rate"]

            item_name_pk, uom_name = getOrCreateItem(
                item_name=item_name,
                item_code=item_code,
                stock_uom=stock_uom,
                valuation_rate=basic_rate,
                allow_negative_stock=True,
            )
            itemDict = createStockEntryItemDict(
                item_code=item_name_pk,
                qty=item["qty"],
                uom=uom_name,
                basic_rate=basic_rate,
            )
            itemsDict.append(itemDict)

        createStockEntry(
            itemsDict=itemsDict,
            to_warehouse=to_warehouse_pk,
            from_warehouse=from_warehouse_pk,
            item_inout=item_inout,
            posting_date=posting_date,
        )
        self.assertIsNone(None)
