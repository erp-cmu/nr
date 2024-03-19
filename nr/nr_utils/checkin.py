import frappe
from datetime import datetime
from dateutil.parser import parse
from nr.nr_utils.employee import findEmployee, createEmployee


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

    emp_name, emp_first_name = createOrUpdateEmployeeNameFromAttnDeviceID(
        attendance_device_id
    )

    isCheckin = frappe.db.exists(
        "Employee Checkin",
        {
            "employee": emp_name,
            "time": time,
            "log_type": log_type,
        },
    )
    if isCheckin:
        frappe.msgprint(f"Already check in: {emp_first_name} @ {time} ({log_type})")
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
        frappe.msgprint(f"Checkin successfully: {emp_first_name} @ {time} ({log_type})")

    return None
