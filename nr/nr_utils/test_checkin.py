import frappe
import unittest
from nr.nr_utils.checkin import createCheckin
import random
from datetime import datetime


def create_events():
    if frappe.flags.test_events_created:
        return

    frappe.set_user("Administrator")
    frappe.flags.test_events_created = True


class TestEvent(unittest.TestCase):
    def setUp(self):
        frappe.set_user("Administrator")

    def tearDown(self):
        pass

    def test_checkins(self):
        frappe.set_user("Administrator")
        random_ADID = f"EMP_1000"
        random_time = "2024-03-14 10:00:00"
        random_log_type = "IN"

        shift_type_names = frappe.db.get_all("Shift Type")
        if len(shift_type_names) == 0:
            frappe.throw("Please create at least one shift type")
        default_shift_type = shift_type_names[0]["name"]

        createCheckin(
            attendance_device_id=random_ADID,
            log_type=random_log_type,
            time=random_time,
            default_shift_type=default_shift_type,
        )
        self.assertIsNone(None)

    def test_checkins_no_emp(self):
        frappe.set_user("Administrator")
        random_ADID = f"EMP_{random.randint(1000, 9999)}"
        random_time = datetime.now()
        random_log_type = random.choice(["IN", "OUT"])

        shift_type_names = frappe.db.get_all("Shift Type")
        if len(shift_type_names) == 0:
            frappe.throw("Please create at least one shift type")
        default_shift_type = shift_type_names[0]["name"]

        createCheckin(
            attendance_device_id=random_ADID,
            log_type=random_log_type,
            time=random_time,
            default_shift_type=default_shift_type,
        )
        self.assertIsNone(None)
