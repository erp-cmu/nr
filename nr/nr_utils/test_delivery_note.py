# bench --site mysite run-tests --module "nr.nr_utils.test_delivery_note"

import frappe
import unittest
from nr.nr_utils.sales_invoice import *
from nr.nr_utils.item import getOrCreateItem
from nr.nr_utils.sales_order import *
from nr.nr_utils.customer import *
from datetime import datetime
from nr.nr_utils.payment_entry import *
from nr.nr_utils.delivery_note import *


def create_events():
    if frappe.flags.test_events_created:
        return

    frappe.set_user("Administrator")
    frappe.flags.test_events_created = True


class TestDeliveryNote(unittest.TestCase):
    def setUp(self):
        frappe.set_user("Administrator")

    def tearDown(self):
        pass

    def test_delivery_note(self):
        customer_name = "customer 8"
        item_code = "Item 8"
        rate = 1000
        qty = 10
        now = datetime.now()
        due_date = now.strftime("%Y-%m-%d")
        delivery_date = due_date
        customer_name_pk = getOrCreateCustomer(customer_name=customer_name)
        item_code_pk = getOrCreateItem(
            item_code=item_code, item_name=item_code, allow_negative_stock=True
        )

        # Create sales order
        itemsDict = []
        item = createSalesOrderItemDict(item_code=item_code_pk, qty=qty, rate=rate)
        itemsDict.append(item)
        sales_order_pk = createSalesOrder(
            customer_name=customer_name_pk,
            delivery_date=delivery_date,
            itemsDict=itemsDict,
        )

        # Create sales invoice
        itemsDict = []
        item = createSalesInvoiceItemDict(
            item_code=item_code_pk, qty=qty, rate=rate, sales_order=sales_order_pk
        )
        itemsDict.append(item)
        #
        sales_invoice_pk = createSalesInvoice(
            itemsDict=itemsDict, due_date=due_date, customer_name=customer_name_pk
        )

        # Create delivery note

        itemsDict = []
        so_detail = getSalesOrderItem(
            sales_order_name=sales_order_pk, item_code=item_code_pk
        )
        si_detail = getSalesInvoiceItem(
            sales_invoice_name=sales_invoice_pk, item_code=item_code_pk
        )
        item = createDeliveryNoteItemDict(
            item_code=item_code_pk,
            qty=qty,
            rate=rate,
            against_sales_order=sales_order_pk,
            so_detail=so_detail,
            against_sales_invoice=sales_invoice_pk,
            si_detail=si_detail,
        )
        itemsDict.append(item)
        createDeliveryNote(customer_name=customer_name, itemsDict=itemsDict)

        # Update status
        # updateSalesOrderStatus(
        #     sales_order_name=sales_order_pk, is_billed=True, is_delivered=False
        # )
        pass
