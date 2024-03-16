import frappe
from frappe.utils import getdate, today, add_to_date
from datetime import datetime, date
from dateutil.parser import parse
import pandas as pd


def createOrGetEmployeeFromADI(attendance_device_id):
    if not attendance_device_id:
        frappe.throw("Unknown attendance_device_id")
    # frappe.db.exists({"doctype":"Employee","attendance_device_id":})

    resADD = frappe.db.get_list(
        "Employee", filters={"attendance_device_id": attendance_device_id}
    )

    if len(resADD) == 0:

        resFirstName = frappe.db.get_list(
            "Employee", filters={"first_name": attendance_device_id}
        )

        todayDT = getdate(today())
        date_of_joining = add_to_date(todayDT, years=-1)
        date_of_birth = add_to_date(todayDT, years=-30)

        if len(resFirstName) == 0:
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
        else:
            emp_name = resFirstName[0].name
            print("resFirstName", emp_name)
    else:
        emp_name = resADD[0].name
        print("resAdd", emp_name)

    return emp_name


def NRparse(string, agnostic=True, **kwargs):
    if agnostic or parse(string, **kwargs) == parse(
        string, yearfirst=True, **kwargs
    ) == parse(string, dayfirst=True, **kwargs):
        return parse(string, **kwargs)
    else:
        raise ValueError("The date was ambiguous: %s" % string)


@frappe.whitelist(allow_guest=True)
def createCheckins(attendance_device_id, log_type, time, device_id="DEFAULT"):

    if log_type not in ["IN", "OUT"]:
        frappe.throw("Invalid log_type")

    if (type(time) is not datetime) and (type(time) is not str):
        frappe.throw("Please use datetime or string for time.")

    if type(time) is str:
        try:
            time = NRparse(time)
        except:
            frappe.throw("Cannot parse date string.")

    emp_name = createOrGetEmployeeFromADI(attendance_device_id)

    doc = frappe.db.exists(
        "Employee Checkin",
        {
            "employee": emp_name,
            "time": time,
            "log_type": log_type,
        },
    )
    if doc:
        frappe.msgprint("Already check in")
    else:
        doc = frappe.get_doc(
            {
                "doctype": "Employee Checkin",
                "employee": emp_name,
                "log_type": log_type,
                "time": time,
                "device_id": device_id,
            }
        )

        doc.insert(ignore_if_duplicate=True)

    return None


def formatTorDrinkExcelP1(row):
    name = row["ชื่อ-นามสกุล"]
    id = row["รหัสที่เครื่อง"]
    dateStr = row["Date"]
    sp = dateStr.split("/")
    day = sp[0]
    month = sp[1]
    year = int(sp[2]) - 543
    times = row.iloc[5:].dropna()
    if len(times) == 0:
        return pd.Series({"name": name, "id": id, "min": pd.NaT, "max": pd.NaT})
    times = times.apply(
        lambda t: pd.to_datetime(f"{year}/{month}/{day} {t}", format="%Y/%m/%d %H:%M")
    )
    res = times.agg(["min", "max"])
    res["name"] = name
    res["id"] = id
    return res


def formatTorDrinkExcelP2(row):
    datas = []
    for i in ["IN", "OUT"]:
        data = {
            "attendance_device_id": row["name"],
            "log_type": i,
            "time": row[i].strftime("%Y/%m/%d %X"),
        }
        datas.append(data)
    return pd.DataFrame.from_records(datas)


def processExcelTorDrink(filepath):
    dft = pd.read_excel(filepath)
    df1 = dft.iloc[:, :].apply(formatTorDrinkExcelP1, axis=1)
    df1.dropna(inplace=True)
    df1.rename(columns={"min": "IN", "max": "OUT"}, inplace=True)
    temp = df1.iloc[:, :].apply(formatTorDrinkExcelP2, axis=1)
    df2 = pd.concat(temp.values).reset_index(drop=True)

    return df2
