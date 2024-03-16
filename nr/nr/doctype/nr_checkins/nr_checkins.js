// Copyright (c) 2024, IECMU and contributors
// For license information, please see license.txt

frappe.ui.form.on("NR Checkins", {
  refresh(frm) {
    // frm.add_custom_button("AAA", ()=>{})
    // frappe.msgprint('A row has been added to the links table 🎉 ');
    // frappe.set_route('List', 'Task', 'List')
    frm.add_custom_button("Run", function () {
      frappe.call({
        method: "nr.nr.doctype.nr_checkins.utils.createCheckins",
        type: "POST",
        args: {
          attendance_device_id: "AAA",
          log_type: "IN",
          time: "2023/03/16 10:24:11",
        },
        callback: function (res) {
          console.log(res);
          frappe.msgprint("A row has been added to the links table 🎉 ");
        },
      });
    });
  },
});
