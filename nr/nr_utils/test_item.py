# bench --site mysite run-tests --module "nr.nr_utils.test_item"

import frappe
import unittest
from nr.nr_utils.item import getOrCreateItem, getOrCreateUOM, getOrCreateItemGroup
from nr.nr_utils.warehouse import getOrCreateWarehouse
from nr.nr_utils.stock_entry import createStockEntry, createStockEntryItemDict


def create_events():
    if frappe.flags.test_events_created:
        return

    frappe.set_user("Administrator")
    frappe.flags.test_events_created = True


class TestItem(unittest.TestCase):
    def setUp(self):
        frappe.set_user("Administrator")

    def tearDown(self):
        pass

    def test_item(self):

        # Input
        item_group_name = "ITEM_GROUP_1"
        uom_name = "UOM_1"
        parent_warehouse_name = "PARENT_WAREHOUSE_1"
        warehouse_name = "WAREHOUSE_1"
        item_code = "ITEM002"
        item_name = "ITEMNAME002"
        opening_stock = 120
        valuation_rate = 200
        allow_negative_stock = False

        # Create item group
        item_group_name_pk = getOrCreateItemGroup(item_group_name=item_group_name)

        # Create UOM
        uom_name_pk = getOrCreateUOM(uom_name=uom_name, must_be_whole_number=False)

        # Create parent warehouse
        parent_warehouse_pk = getOrCreateWarehouse(
            parent_warehouse_name, parent_warehouse=None, is_group=True
        )

        # Create warehouse
        warehouse_pk = getOrCreateWarehouse(
            warehouse_name,
            parent_warehouse=parent_warehouse_pk,
        )

        # Create item
        item_name_pk, uom_name = getOrCreateItem(
            item_code=item_code,
            item_name=item_name,
            item_group=item_group_name_pk,
            stock_uom=uom_name_pk,
            opening_stock=0,
            allow_negative_stock=allow_negative_stock,
            valuation_rate=valuation_rate,
        )

        # Create opening stock
        if opening_stock > 0:
            qty = opening_stock
            itemDict = createStockEntryItemDict(
                item_code=item_name_pk, qty=qty, uom=uom_name
            )
            itemsDict = [itemDict]
            createStockEntry(
                itemsDict=itemsDict, to_warehouse=warehouse_pk, item_inout="IN"
            )

        self.assertIsNone(None)
