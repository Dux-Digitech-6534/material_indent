// Copyright (c) 2026, shubhangi pawar and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Material Indent", {
// 	refresh(frm) {

// 	},
// });


frappe.ui.form.on('Material Indent', {
    onload: function(frm) {
        if (frm.is_new()) {

            frappe.db.get_doc('User', frappe.session.user)
                .then(user => {

                    let full_name = user.full_name || '';
                    let department = user.department || '';
                    let company = user.company || '';

                    // agar company empty ho to skip ho jayega
                    let final_value = [
                        full_name,
                        department,
                        company
                    ].filter(Boolean).join(' - ');

                    frm.set_value('user', final_value);
                });

        }
    }
});



frappe.ui.form.on('Material Request Item', {

    item_code: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];

        if (!row.item_code) return;

        // Item ka data lao
        frappe.db.get_doc("Item", row.item_code).then(item => {

            // ✅ Default UOM set karo
            if (item.stock_uom) {
                frappe.model.set_value(cdt, cdn, "uom", item.stock_uom);
            }

        });
    }

});


frappe.ui.form.on('Material Request Item', {

    table_feob_add: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];

        if (frm.doc.required_by) {
            frappe.model.set_value(cdt, cdn, "required_by", frm.doc.required_by);
        }
    }

});