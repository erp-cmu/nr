import frappe
from frappe.utils import getdate, today, add_to_date
def createOrGetEmployeeFromADI(attendance_device_id):
    if not attendance_device_id:
        frappe.throw('Unknown attendance_device_id')
    # frappe.db.exists({"doctype":"Employee","attendance_device_id":})

    resADD = frappe.db.get_list("Employee", filters={
        'attendance_device_id': attendance_device_id
    })
    
    if len(resADD) == 0:

        resFirstName = frappe.db.get_list("Employee", filters={
            'first_name': attendance_device_id
        })
        
        todayDT = getdate(today())
        date_of_joining = add_to_date(todayDT, years=-1)
        date_of_birth = add_to_date(todayDT, years=-30)
        
        if len(resFirstName) == 0:
            newEmp = frappe.get_doc({
                    "doctype": "Employee",
                    "first_name": attendance_device_id,
                    "attendance_device_id": attendance_device_id,
                    "date_of_joining": date_of_joining,
                    "date_of_birth": date_of_birth,
                    "gender": "Male"
                })
            newEmp.insert()        
        else:
            emp_name = resFirstName[0].name         
            print('resFirstName', emp_name)            
    else:
        emp_name = resADD[0]
        print('resAdd', emp_name)
    
    return emp_name

@frappe.whitelist(allow_guest=True)
def createCheckins(attendance_device_id):
    
    emp_name = createOrGetEmployeeFromADI(attendance_device_id)
    
    doc = frappe.get_doc({
        "doctype": "Employee Checkin",
        "employee": emp_name,
        "log_type": "IN",
        "time": getdate(today())
    })
    doc.insert()
    print('------------Done-----------------')
    return None