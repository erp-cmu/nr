import frappe
from frappe.utils import getdate, today, add_to_date


def findEmployee(searchStr):

    searchStr = searchStr.strip()

    name = frappe.db.exists(
        "Employee",
        {
            "first_name": searchStr,
        },
    )

    if name:
        return name

    name = frappe.db.exists(
        "Employee",
        {
            "last_name": searchStr,
        },
    )

    if name:
        return name

    name = frappe.db.exists(
        "Employee",
        {
            "employee_name": searchStr,
        },
    )

    if name:
        return name
    else:
        return None


def createEmployee(fullname, attendance_device_id=None):

    fullname = fullname.strip()
    sp = fullname.split(" ")
    first_name = sp[0]
    last_name = ""
    if len(sp) > 1:
        last_name = " ".join(sp[1:])

    if not attendance_device_id:
        attendance_device_id = fullname

    todayDT = getdate(today())
    date_of_joining = add_to_date(todayDT, years=-1)
    date_of_birth = add_to_date(todayDT, years=-30)
    doc = frappe.get_doc(
        {
            "doctype": "Employee",
            "first_name": first_name,
            "last_name": last_name,
            "attendance_device_id": attendance_device_id,
            "date_of_joining": date_of_joining,
            "date_of_birth": date_of_birth,
            "gender": "Male",
        }
    )
    newEmp = doc.insert()
    return newEmp.name, newEmp.first_name


def createOrUpdateEmployeeNameFromAttnDeviceID(attendance_device_id):

    nameFromADID = frappe.db.exists(
        "Employee",
        {
            "attendance_device_id": attendance_device_id,
        },
    )

    nameFromSearch = findEmployee(attendance_device_id)

    emp_name = None
    emp_first_name = None

    if nameFromADID:
        # Found user with ADID
        emp_name = nameFromADID
        emp_first_name = frappe.db.get_value("Employee", emp_name, "first_name")
    else:
        if nameFromSearch:
            # User found without ADID, add one
            frappe.db.set_value(
                "Employee",
                nameFromSearch,
                "attendance_device_id",
                attendance_device_id,
            )
            emp_name = nameFromSearch
            emp_first_name = nameFromSearch
        else:
            # No user found, create user with random info
            emp_name, emp_first_name = createEmployee(
                fullname=attendance_device_id, attendance_device_id=attendance_device_id
            )

    return emp_name, emp_first_name
