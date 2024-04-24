# bench --site mysite run-tests --module "nr.nr_utils.test_sales_invoice"

import frappe
import unittest
from nr.nr_utils.sales_invoice import *
from nr.nr_utils.item import getOrCreateItem
from nr.nr_utils.sales_order import *
from nr.nr_utils.customer import *
from datetime import datetime


def create_events():
    if frappe.flags.test_events_created:
        return

    frappe.set_user("Administrator")
    frappe.flags.test_events_created = True


class TestSalesInvoice(unittest.TestCase):
    def setUp(self):
        frappe.set_user("Administrator")

    def tearDown(self):
        pass

    def test_sales_order(self):

        # customer_name = "customer 4"
        # item_code = "Item 4"
        # rate = 300
        # qty = 10
        #
        # now = datetime.now()
        # delivery_date = now.strftime("%Y-%m-%d")
        #
        # customer_name_pk = getOrCreateCustomer(customer_name=customer_name)
        # item_code_pk = getOrCreateItem(item_code=item_code, item_name=item_code)
        # itemsDict = []
        # item = createSalesOrderItemDict(item_code=item_code_pk, qty=qty, rate=rate)
        # itemsDict.append(item)
        #
        createSalesInvoice()
