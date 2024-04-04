import frappe
import unittest
from nr.nr_utils.item import createItem, createUOM, createItemGroup
from nr.nr_utils.warehouse import getOrCreateWarehouse
import random
from datetime import datetime
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

    def test_item(self):

        item_group_name = "GGG"
        item_group_name_pk = createItemGroup(item_group_name=item_group_name)

        uom_name = "AAA"
        uom_name_pk = createUOM(uom_name=uom_name)

        parent_warehouse_pk = getOrCreateWarehouse(
            "Test", parent_warehouse=None, is_group=True
        )

        warehouse_pk = getOrCreateWarehouse(
            "CCC",
            parent_warehouse=parent_warehouse_pk,
        )

        item_code = "ITEM001"
        item_name = "ITEMNAME001"
        createItem(
            item_code=item_code,
            item_name=item_name,
            item_group=item_group_name_pk,
            stock_uom=uom_name_pk,
            opening_stock=10,
        )        
        qty = 101
        itemDict = createStockEntryItemDict(
            item_code=item_code,
            qty=qty,
        )
        itemsDict = [itemDict]

        createStockEntry(
            itemsDict=itemsDict, to_warehouse=warehouse_pk, item_inout="IN"
        )
 
        self.assertIsNone(None)
