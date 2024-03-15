// Copyright (c) 2024, IECMU and contributors
// For license information, please see license.txt

frappe.ui.form.on("NR Checkins", {
    refresh(frm) {
        // frm.add_custom_button("AAA", ()=>{})
        // frappe.msgprint('A row has been added to the links table 🎉 ');
        frm.add_custom_button("Run", function () {
            // frappe.set_route('List', 'Task', 'List')
            // frappe.call({
            //     method: "ext_erp_int.ext_erp_int.doctype.eei_upload"
            // })
        });
    },
});
