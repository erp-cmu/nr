# bench --site mysite run-tests --module "nr.nr_utils.test_auto_sales_logic"

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


class TestAutoSales(unittest.TestCase):
    def setUp(self):
        frappe.set_user("Administrator")

    def tearDown(self):
        pass

    def test_auto_sales(self):
        # Input
        customer_name = "Customer 3"
        custom_external_sales_order_id = "CUSTOM705"
        # NOTE: I include options for valuation rate here.
        itemsArray = [
            dict(
                item_code="ITEM005",
                item_name="Item 5",
                rate=300,
                qty=0.25,
                # valuation_rate=300,
            ),
            dict(
                item_code="ITEM006",
                item_name="Item 6",
                rate=200,
                qty=0.25,
                # valuation_rate=200,
            ),
        ]
        # now = datetime.now()
        # delivery_date = now.strftime("%Y-%m-%d")
        # due_date = now.strftime("%Y-%m-%d")
        # posting_date = now.strftime("%Y-%m-%d")

        delivery_date = "2024-04-01"
        due_date = delivery_date
        posting_date = delivery_date

        # Logic
        customer_name_pk = getOrCreateCustomer(customer_name=customer_name)

        # Create sales order
        itemsDict = []
        for itemsArrayEle in itemsArray:
            item_code = itemsArrayEle["item_code"]
            item_name = itemsArrayEle["item_name"]
            rate = itemsArrayEle["rate"]
            qty = itemsArrayEle["qty"]
            # valuation_rate = itemsArrayEle["valuation_rate"]
            item_code_pk, uom_name = getOrCreateItem(
                item_code=item_code,
                item_name=item_name,
                allow_negative_stock=True,
                # valuation_rate=valuation_rate,
            )
            item = createSalesOrderItemDict(
                item_code=item_code_pk, qty=qty, rate=rate, uom=uom_name
            )
            itemsDict.append(item)
        sales_order_pk = createSalesOrder(
            customer_name=customer_name_pk,
            delivery_date=delivery_date,
            itemsDict=itemsDict,
            custom_external_sales_order_id=custom_external_sales_order_id,
        )

        # Create sales invoice
        itemsDict = []
        for itemsArrayEle in itemsArray:

            item_code = itemsArrayEle["item_code"]
            item_name = itemsArrayEle["item_name"]
            rate = itemsArrayEle["rate"]
            qty = itemsArrayEle["qty"]

            item_code_pk, _ = getOrCreateItem(
                item_code=item_code, item_name=item_name, allow_negative_stock=True
            )
            so_detail = getSalesOrderItem(
                sales_order_name=sales_order_pk, item_code=item_code_pk
            )

            item = createSalesInvoiceItemDict(
                item_code=item_code_pk,
                qty=qty,
                rate=rate,
                sales_order=sales_order_pk,
                so_detail=so_detail,
            )
            itemsDict.append(item)
        #
        sales_invoice_pk = createSalesInvoice(
            itemsDict=itemsDict, due_date=due_date, customer_name=customer_name_pk
        )

        # Create delivery note
        itemsDict = []
        for itemsArrayEle in itemsArray:

            item_code = itemsArrayEle["item_code"]
            item_name = itemsArrayEle["item_name"]
            rate = itemsArrayEle["rate"]
            qty = itemsArrayEle["qty"]

            item_code_pk, _ = getOrCreateItem(
                item_code=item_code, item_name=item_name, allow_negative_stock=True
            )
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

        createDeliveryNote(
            customer_name=customer_name,
            itemsDict=itemsDict,
            posting_date=posting_date,
        )

        # Create payment entry
        itemsDict = []
        total_amount = 0
        for itemsArrayEle in itemsArray:
            rate = itemsArrayEle["rate"]
            qty = itemsArrayEle["qty"]
            total_amount = total_amount + rate * qty

        # We only need to create one payment reference to sales invoice (even for multiple items).
        item = createPaymentReferencesItemDict(
            reference_name=sales_invoice_pk,
            total_amount=total_amount,
            allocated_amount=total_amount,
            outstanding_amount=total_amount,
        )
        itemsDict.append(item)
        createPaymentEntryReceive(
            customer_name=customer_name_pk,
            received_amount=total_amount,
            itemsDict=itemsDict,
        )

        # Update status
        updateSalesOrderStatus(
            sales_order_name=sales_order_pk, is_billed=True, is_delivered=True
        )
        pass
