import frappe

@frappe.whitelist(allow_guest=True)
def checkEmployee(attendance_device_id):

    # frappe.db.exists({"doctype":"Employee","attendance_device_id":})
    
    res = frappe.db.get_list("Employee", filters={
        'attendance_device_id': attendance_device_id
    })
    
    print(res)
    # doc = frappe.get_doc({
    #     "doctype": "Employee",
    #     "first_name": first_name,
    # })
    # print(doc.first_name)
    # print(doc.attendance_device_id)
    return doc