# bench --site mysite run-tests --module "nr.nr_utils.test_payment_entry"

import frappe
import unittest
from nr.nr_utils.sales_invoice import *
from nr.nr_utils.item import getOrCreateItem
from nr.nr_utils.sales_order import *
from nr.nr_utils.customer import *
from datetime import datetime
from nr.nr_utils.payment_entry import *


def create_events():
    if frappe.flags.test_events_created:
        return

    frappe.set_user("Administrator")
    frappe.flags.test_events_created = True


class TestPaymentEntry(unittest.TestCase):
    def setUp(self):
        frappe.set_user("Administrator")

    def tearDown(self):
        pass

    def test_payment_entry(self):
        createPaymentEntryReceive("Customer 5")
        pass
