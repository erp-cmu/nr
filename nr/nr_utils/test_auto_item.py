# tbench --site mysite run-tests --module "nr.nr_utils.test_auto_item"

import frappe
import unittest
from nr.nr_utils.auto_item_import import processAutoItemImport


def create_events():
    if frappe.flags.test_events_created:
        return

    frappe.set_user("Administrator")
    frappe.flags.test_events_created = True


class TestAutoItem(unittest.TestCase):
    def setUp(self):
        frappe.set_user("Administrator")

    def tearDown(self):
        pass

    def test_auto_item(self):

        itemArray = []

        itemEle = dict(
            # Required
            item_code="CODE_102",
            item_name="NAME_102",
            # Optional
            uom_name="UOM_102",
            warehouse_name="J21",
            item_group_name="ITEM_GROUP_102",
            valuation_rate=300,
            opening_stock=200,
            allow_negative_stock=False,
            parent_warehouse_name="PARENT_WAREHOUSE_2",
            must_be_whole_number=False,
            is_stock_item=True,
        )
        itemArray.append(itemEle)

        itemEle = {
            **itemEle,
            "warehouse_name": "J22",
        }
        itemArray.append(itemEle)

        for item in itemArray:
            processAutoItemImport(
                item_name=item["item_name"],
                item_code=item["item_code"],
                opening_stock=item["opening_stock"],
                warehouse_name=item["warehouse_name"],
                must_be_whole_number=item["must_be_whole_number"],
                allow_negative_stock=item["allow_negative_stock"],
                valuation_rate=item["valuation_rate"],
                # item_group_name=item["item_group_name"],
                uom_name=item["uom_name"],
                # parent_warehouse_name=item["parent_warehouse_name"],
                is_stock_item=item["is_stock_item"],
            )

        self.assertIsNone(None)
