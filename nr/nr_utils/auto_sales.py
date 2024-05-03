from nr.nr_utils.sales_invoice import (
    createSalesInvoice,
    createSalesInvoiceItemDict,
    getSalesInvoiceItem,
)
from nr.nr_utils.item import getOrCreateItem, makeUOMFractional
from nr.nr_utils.sales_order import (
    createSalesOrder,
    getSalesOrderItem,
    updateSalesOrderStatus,
    createSalesOrderItemDict,
    checkCustomExternalSalesOrderID,
)
from nr.nr_utils.customer import getOrCreateCustomer
from nr.nr_utils.payment_entry import (
    createPaymentEntryReceive,
    createPaymentReferencesItemDict,
)
from nr.nr_utils.delivery_note import createDeliveryNote, createDeliveryNoteItemDict
import frappe


def processAutoSale(
    customer_name,
    itemsArray,
    delivery_date,
    due_date,
    posting_date,
    custom_external_sales_order_id,
    custom_sales_order_source="OTHER",
):
    # NOTE: This process does not take into account valuation rate.
    # Example of itemArray
    # itemsArray = [
    #     dict(
    #         item_code="ITEM005",
    #         item_name="Item 5",
    #         rate=300,
    #         qty=10,
    #     ),
    #     dict(
    #         item_code="ITEM006",
    #         item_name="Item 6",
    #         rate=200,
    #         qty=20,
    #     ),
    # ]

    # NOTE: skip this process if external id exists
    id = checkCustomExternalSalesOrderID(id=custom_external_sales_order_id)
    if id:
        frappe.msgprint(
            msg=f"Skip importing [{custom_external_sales_order_id}] due to duplicated external id in [{id}]."
        )
        return

    customer_name_pk = getOrCreateCustomer(customer_name=customer_name)

    # Create sales order
    itemsDict = []
    for itemsArrayEle in itemsArray:
        item_code = itemsArrayEle["item_code"]
        item_name = itemsArrayEle["item_name"]
        rate = itemsArrayEle["rate"]
        qty = itemsArrayEle["qty"]

        item_code_pk, uom_name = getOrCreateItem(
            item_code=item_code,
            item_name=item_name,
            allow_negative_stock=True,
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
        custom_sales_order_source=custom_sales_order_source,
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
