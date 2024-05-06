# bench --site mysite run-tests --module "nr.nr_utils.test_auto_item"

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

        # Required
        item_code = "CODE_102"
        item_name = "NAME_102"

        # Optional
        uom_name = "UOM_102"
        warehouse_name = "J5"
        item_group_name = "ITEM_GROUP_102"
        valuation_rate = 300
        opening_stock = 200
        allow_negative_stock = False
        parent_warehouse_name = "PARENT_WAREHOUSE_2"
        must_be_whole_number = False

        processAutoItemImport(
            item_name=item_name,
            item_code=item_code,
            opening_stock=opening_stock,
            warehouse_name=warehouse_name,
            must_be_whole_number=must_be_whole_number,
            allow_negative_stock=allow_negative_stock,
            valuation_rate=valuation_rate,
            # item_group_name=item_group_name,
            uom_name=uom_name,
            # parent_warehouse_name=parent_warehouse_name,
        )

        self.assertIsNone(None)
