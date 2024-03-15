import frappe
import json

@frappe.whitelist(allow_guest=True)
def ping(*args, **kwargs):
	print(args)
	print(kwargs)
	# doc = frappe.new_doc("Item")
	# doc.item_code = name
	# doc.item_name = name
	# doc.item_group = "Products"
	# doc.insert()
	return "yes"