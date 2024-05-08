from nr.nr_utils.item import getOrCreateItem, getOrCreateUOM, getOrCreateItemGroup
from nr.nr_utils.warehouse import getOrCreateWarehouse
from nr.nr_utils.stock_entry import createStockEntry, createStockEntryItemDict


def processAutoItemImport(
    item_name,
    item_code,
    opening_stock=0,
    valuation_rate=0,
    allow_negative_stock=False,
    item_group_name="DEFAULT",
    uom_name="Nos",
    warehouse_name="TEMP",
    parent_warehouse_name="CUSTOM",
    must_be_whole_number=False,
    is_stock_item=True,
):

    # Create item group
    item_group_name_pk = getOrCreateItemGroup(item_group_name=item_group_name)

    # Create UOM
    uom_name_pk = getOrCreateUOM(
        uom_name=uom_name, must_be_whole_number=must_be_whole_number
    )

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
    itemData = dict(
        item_code=item_code,
        item_name=item_name,
        item_group=item_group_name_pk,
        stock_uom=uom_name_pk,
        opening_stock=0,
        allow_negative_stock=allow_negative_stock,
        is_stock_item=is_stock_item,
    )
    if valuation_rate:
        itemData["valuation_rate"] = valuation_rate
    item_name_pk, uom_name = getOrCreateItem(**itemData)

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
