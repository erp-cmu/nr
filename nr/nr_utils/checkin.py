import frappe
from datetime import datetime
from nr.nr_utils.employee import createOrUpdateEmployeeNameFromAttnDeviceID
from nr.nr_utils.common import date_parse
from nr.nr_utils.shift_assignment import handleShiftAssignment


def createCheckin(
    attendance_device_id, log_type, time, default_shift_type, device_id="DEFAULT"
):

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

    shift_type = handleShiftAssignment(
        emp_name=emp_name, default_shift_type=default_shift_type
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
                "shift": shift_type,
            }
        )
        newCheckin.insert(ignore_if_duplicate=True)
        frappe.msgprint(f"Checkin successfully: {emp_first_name} @ {time} ({log_type})")

    return None
