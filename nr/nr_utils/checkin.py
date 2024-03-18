import frappe
from frappe.utils import getdate, today, add_to_date
from datetime import datetime
from dateutil.parser import parse


def createOrUpdateEmployeeNameFromAttnDeviceID(attendance_device_id):

    nameFromADID = frappe.db.exists(
        "Employee",
        {
            "attendance_device_id": attendance_device_id,
        },
    )

    nameFromFirstName = frappe.db.exists(
        "Employee",
        {
            "first_name": attendance_device_id,
        },
    )

    emp_name = None

    if nameFromADID:
        # Found user with ADID
        emp_name = nameFromADID
    else:
        if nameFromFirstName:
            # User found without ADID, add one
            frappe.db.set_value(
                "Employee",
                nameFromFirstName,
                "attendance_device_id",
                attendance_device_id,
            )
            emp_name = nameFromFirstName
        else:
            # No user found, create user with random info
            todayDT = getdate(today())
            date_of_joining = add_to_date(todayDT, years=-1)
            date_of_birth = add_to_date(todayDT, years=-30)
            newEmp = frappe.get_doc(
                {
                    "doctype": "Employee",
                    "first_name": attendance_device_id,
                    "attendance_device_id": attendance_device_id,
                    "date_of_joining": date_of_joining,
                    "date_of_birth": date_of_birth,
                    "gender": "Male",
                }
            )
            doc = newEmp.insert()
            emp_name = doc.name

    return emp_name


def date_parse(string, agnostic=True, **kwargs):
    if agnostic or parse(string, **kwargs) == parse(
        string, yearfirst=True, **kwargs
    ) == parse(string, dayfirst=True, **kwargs):
        return parse(string, **kwargs)
    else:
        raise ValueError("The date was ambiguous: %s" % string)


def createCheckin(attendance_device_id, log_type, time, device_id="DEFAULT"):

    if log_type not in ["IN", "OUT"]:
        frappe.throw("Invalid log_type")

    if (type(time) is not datetime) and (type(time) is not str):
        frappe.throw("Please use datetime or string for time.")

    if type(time) is str:
        try:
            time = date_parse(time)
        except:
            frappe.throw("Cannot parse date string.")

    emp_name = createOrUpdateEmployeeNameFromAttnDeviceID(attendance_device_id)

    isCheckin = frappe.db.exists(
        "Employee Checkin",
        {
            "employee": emp_name,
            "time": time,
            "log_type": log_type,
        },
    )
    if isCheckin:
        frappe.msgprint(f"Already check in: {emp_name} @ {time} ({log_type})")
    else:
        newCheckin = frappe.get_doc(
            {
                "doctype": "Employee Checkin",
                "employee": emp_name,
                "log_type": log_type,
                "time": time,
                "device_id": device_id,
            }
        )
        newCheckin.insert(ignore_if_duplicate=True)
        frappe.msgprint(f"Checkin successfully: {emp_name} @ {time} ({log_type})")

    return None
