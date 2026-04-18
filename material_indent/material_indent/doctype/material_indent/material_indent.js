// // Copyright (c) 2026, shubhangi pawar and contributors
// // For license information, please see license.txt

// // frappe.ui.form.on("Material Indent", {
// // 	refresh(frm) {

// // 	},
// // });






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

                    frm.set_value('custom_username', final_value);
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



frappe.ui.form.on('Material Indent', {

    refresh: function(frm) {
        console.log("Form Loaded");
    },

    required_by: function(frm) {
        console.log("Required By Changed:", frm.doc.required_by);

        if (frm.doc.required_by) {
            (frm.doc.table_feob || []).forEach(function(row) {
                row.schedule_date = frm.doc.required_by;
            });

            frm.refresh_field('table_feob');
        }
    }

});


frappe.ui.form.on('Material Request Item', {

    table_feob_add: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];

        console.log("Row Added:", row);

        if (frm.doc.required_by) {
            row.schedule_date = frm.doc.required_by;
        }

        frm.refresh_field('table_feob');
    }

});


frappe.ui.form.on('Material Indent', {});



// view stock poup 




frappe.ui.form.on('Material Indent', {
    refresh: function(frm) {

        frm.fields_dict.table_feob.grid.wrapper.on('click', function() {
            setTimeout(() => {
                toggle_button(frm);
            }, 200);
        });

        toggle_button(frm);
    }
});

function toggle_button(frm) {

    frm.clear_custom_buttons();

    let selected_items = frm.get_selected().table_feob || [];

    if (selected_items.length > 0) {

        frm.add_custom_button('View Stock', function() {

            let d = new frappe.ui.Dialog({
                title: 'Stock Details (All Warehouses)',
                size: 'extra-large',
                fields: [
                    { fieldname: 'stock_table', fieldtype: 'HTML' }
                ]
            });

            let html = `
                <table class="table table-bordered">
                    <thead>
                        <tr>
                            <th>Item Code</th>
                            <th>Company</th>
                            <th>Warehouse</th>
                            <th>Available Qty</th>
                        </tr>
                    </thead>
                    <tbody id="stock-body">
                        <tr>
                            <td colspan="4" style="text-align:center;">Loading...</td>
                        </tr>
                    </tbody>
                </table>
            `;

            d.fields_dict.stock_table.$wrapper.html(html);
            d.show();

            let rows = "";
            let completed = 0;

            selected_items.forEach(row_name => {

                let item = frm.doc.table_feob.find(i => i.name === row_name);
                if (!item) return;

                // 🔥 IMPORTANT: Get all warehouse stock
                frappe.call({
                    method: "frappe.client.get_list",
                    args: {
                        doctype: "Bin",
                        filters: {
                            item_code: item.item_code
                        },
                        fields: ["warehouse", "actual_qty"]
                    },
                    callback: function(r) {

                        if (r.message && r.message.length > 0) {

                            r.message.forEach(bin => {

                                if (bin.actual_qty > 0) {

                                    rows += `
                                        <tr>
                                            <td>${item.item_code}</td>
                                            <td>${frm.doc.company}</td>
                                            <td>${bin.warehouse}</td>
                                            <td style="color:${bin.actual_qty < 10 ? 'red' : 'green'}">
                                                ${bin.actual_qty}
                                            </td>
                                        </tr>
                                    `;
                                }

                            });

                        }

                        completed++;

                        if (completed === selected_items.length) {

                            d.fields_dict.stock_table.$wrapper
                                .find("#stock-body")
                                .html(
                                    rows || `<tr><td colspan="4" style="text-align:center;">No Stock Available</td></tr>`
                                );
                        }
                    }
                });

            });

        });

    }
}

// 🔥 PURPOSE BUTTON FINAL (CORRECTED)



frappe.ui.form.on('Material Indent', {
    refresh: function(frm) {

        // ❌ REMOVE THIS (ye issue ka main reason hai)
        // frm.page.clear_actions_menu();

        // ==============================
        // 🔥 MATERIAL ISSUE (POPUP)
        // ==============================
        frm.page.add_action_item(__('Material Issue'), function() {

            let rows = frm.doc.table_feob || [];

            if (!rows.length) {
                frappe.msgprint("❌ Please add items first");
                return;
            }

            let d = new frappe.ui.Dialog({
                title: 'Enter Issue Qty',
                size: 'large',
                fields: rows.map(row => ({
                    fieldtype: 'Float',
                    label: `${row.item_code} (Bal: ${row.custom_qty_balanced || 0})`,
                    fieldname: row.name,
                    default: 0
                })),
                primary_action_label: 'Create Stock Entry',
                primary_action(values) {

                    let items = [];
                    let promises = [];

                    rows.forEach(row => {

                        let qty = values[row.name] || 0;
                        if (qty <= 0) return;

                        let p = frappe.db.get_value("Bin", {
                            item_code: row.item_code,
                            warehouse: row.from_warehouse
                        }, "actual_qty").then(r => {

                            let stock = r.message?.actual_qty || 0;

                            if (qty > stock) {
                                frappe.throw(`❌ Stock not available for ${row.item_code} (Available: ${stock})`);
                            }

                            if (qty > (row.custom_qty_balanced || 0)) {
                                frappe.throw(`❌ Issue qty exceeds balance for ${row.item_code}`);
                            }

                            items.push({
                                item_code: row.item_code,
                                qty: qty,
                                s_warehouse: row.from_warehouse,

                                custom_material_indent: frm.doc.name,
                                custom_material_indent_item: row.name ,
                                   custom_specification:row.custom_specification
                            });

                        });

                        promises.push(p);
                    });

                    Promise.all(promises).then(() => {

                        if (!items.length) {
                            frappe.msgprint("❌ Enter qty first");
                            return;
                        }

                        frappe.call({
                            method: "frappe.client.insert",
                            args: {
                                doc: {
                                    doctype: "Stock Entry",
                                    stock_entry_type: "Material Issue",
                                    company: frm.doc.company,
                                    items: items,
                                     // ✅ ADD THESE
            custom_username: frm.doc.custom_username,
            custom_remark: frm.doc.custom_remark,
            custom_attachment: frm.doc.custome_attachment,
             custom_design: frm.doc.custom_design,
                                }
                            },
                            callback: function(r) {
                                if (r.message) {
                                    frappe.show_alert("✅ Stock Entry Created");
                                    frappe.set_route("Form", "Stock Entry", r.message.name);
                                }
                            }
                        });

                        d.hide();
                    });
                }
            });

            d.show();
        });


        // ==============================
        // 🔥 MATERIAL PURCHASE (POPUP)
        // ==============================
        frm.page.add_action_item(__('Material Purchase'), function() {

            let rows = frm.doc.table_feob || [];

            let d = new frappe.ui.Dialog({
                title: 'Enter Purchase Qty',
                size: 'large',
                fields: rows.map(row => ({
                    fieldtype: 'Float',
                    label: `${row.item_code} (Bal: ${row.custom_qty_balanced || 0})`,
                    fieldname: row.name,
                    default: 0
                })),
                primary_action_label: 'Create Purchase Request',
                primary_action(values) {

                    let items = [];

                    rows.forEach(row => {

                        let qty = values[row.name] || 0;
                        if (qty <= 0) return;

                        if (qty > (row.custom_qty_balanced || 0)) {
                            frappe.throw(`❌ Purchase qty exceeds balance for ${row.item_code}`);
                        }

                        items.push({
                            item_code: row.item_code,
                            qty: qty,
                            schedule_date: frm.doc.required_by,
                            uom: row.uom,

                            custom_material_indent: frm.doc.name,
                            custom_material_indent_item: row.name,
                             custom_specification:row.custom_specification
                        });
                    });

                    if (!items.length) {
                        frappe.msgprint("❌ Enter qty first");
                        return;
                    }

                    frappe.call({
                        method: "frappe.client.insert",
                        args: {
                            doc: {
                                doctype: "Material Request",
                                material_request_type: "Purchase",
                                company: frm.doc.company,
                                items: items,
                                   // ✅ ADD THESE
            custom_username: frm.doc.custom_username,
            custom_remark: frm.doc.custom_remark,
            custom_attachment: frm.doc.custome_attachment,
             custom_design: frm.doc.custom_design,
                            }
                        },
                        callback: function(r) {
                            if (r.message) {
                                frappe.show_alert("✅ Purchase Request Created");
                                frappe.set_route("Form", "Material Request", r.message.name);
                            }
                        }
                    });

                    d.hide();
                }
            });

            d.show();
        });

    }
});



// ==============================
// 🔥 READ ONLY FIELDS
// ==============================
frappe.ui.form.on('Material Indent', {
    refresh: function(frm) {

        frm.fields_dict.table_feob.grid.update_docfield_property(
            'custom_purchase_qty',
            'read_only',
            1
        );

        frm.fields_dict.table_feob.grid.update_docfield_property(
            'custom_issue_qty',
            'read_only',
            1
        );
    }
});


// ==============================
// 🔥 CALCULATION LOGIC
// ==============================
frappe.ui.form.on('Material Request Item', {

    qty: function(frm, cdt, cdn) {
        calculate_remaining(frm, cdt, cdn);
    },

    custom_purchase_qty: function(frm, cdt, cdn) {
        calculate_remaining(frm, cdt, cdn);
    },

    custom_issue_qty: function(frm, cdt, cdn) {
        calculate_remaining(frm, cdt, cdn);
    }
});

function calculate_remaining(frm, cdt, cdn) {

    let row = locals[cdt][cdn];

    let total = flt(row.qty);
    let purchase = flt(row.custom_purchase_qty);
    let issue = flt(row.custom_issue_qty);

    let remaining = total - purchase - issue;

    if (remaining < 0) {
        frappe.msgprint(`❌ Balance negative for ${row.item_code}`);
        remaining = 0;
    }

    row.custom_qty_balanced = remaining;

    frm.refresh_field('table_feob');
}


// ==============================
// 🔥 REFRESH CALCULATION
// ==============================
frappe.ui.form.on('Material Indent', {
    refresh: function(frm) {

        (frm.doc.table_feob || []).forEach(row => {

            let total = flt(row.qty);
            let purchase = flt(row.custom_purchase_qty);
            let issue = flt(row.custom_issue_qty);

            row.custom_qty_balanced = total - purchase - issue;

            if (row.custom_qty_balanced < 0) {
                row.custom_qty_balanced = 0;
            }
        });

        frm.refresh_field('table_feob');
    }
});



























// // Copyright (c) 2026, shubhangi pawar and contributors
// // For license information, please see license.txt

// // frappe.ui.form.on("Material Indent", {
// // 	refresh(frm) {

// // 	},
// // });


// frappe.ui.form.on('Material Indent', {
//     onload: function(frm) {
//         if (frm.is_new()) {

//             frappe.db.get_doc('User', frappe.session.user)
//                 .then(user => {

//                     let full_name = user.full_name || '';
//                     let department = user.department || '';
//                     let company = user.company || '';

//                     // agar company empty ho to skip ho jayega
//                     let final_value = [
//                         full_name,
//                         department,
//                         company
//                     ].filter(Boolean).join(' - ');

//                     frm.set_value('custom_username', final_value);
//                 });

//         }
//     }
// });




// frappe.ui.form.on('Material Request Item', {

//     item_code: function(frm, cdt, cdn) {
//         let row = locals[cdt][cdn];

//         if (!row.item_code) return;

//         // Item ka data lao
//         frappe.db.get_doc("Item", row.item_code).then(item => {

//             // ✅ Default UOM set karo
//             if (item.stock_uom) {
//                 frappe.model.set_value(cdt, cdn, "uom", item.stock_uom);
//             }

//         });
//     }

// });



// frappe.ui.form.on('Material Indent', {

//     refresh: function(frm) {
//         console.log("Form Loaded");
//     },

//     required_by: function(frm) {
//         console.log("Required By Changed:", frm.doc.required_by);

//         if (frm.doc.required_by) {
//             (frm.doc.table_feob || []).forEach(function(row) {
//                 row.schedule_date = frm.doc.required_by;
//             });

//             frm.refresh_field('table_feob');
//         }
//     }

// });


// frappe.ui.form.on('Material Request Item', {

//     table_feob_add: function(frm, cdt, cdn) {
//         let row = locals[cdt][cdn];

//         console.log("Row Added:", row);

//         if (frm.doc.required_by) {
//             row.schedule_date = frm.doc.required_by;
//         }

//         frm.refresh_field('table_feob');
//     }

// });


// frappe.ui.form.on('Material Indent', {});



// // view stock poup 


// frappe.ui.form.on('Material Indent', {
//     refresh: function(frm) {

//         frm.fields_dict.table_feob.grid.wrapper.on('click', function() {
//             setTimeout(() => {
//                 toggle_button(frm);
//             }, 200);
//         });

//         toggle_button(frm);
//     }
// });

// function toggle_button(frm) {

//     frm.clear_custom_buttons();

//     let selected_items = frm.get_selected().table_feob || [];

//     if (selected_items.length > 0) {

//         frm.add_custom_button('View Stock', function() {

//             let d = new frappe.ui.Dialog({
//                 title: 'Stock Details (All Warehouses)',
//                 size: 'extra-large',
//                 fields: [
//                     { fieldname: 'stock_table', fieldtype: 'HTML' }
//                 ]
//             });

//             let html = `
//                 <table class="table table-bordered">
//                     <thead>
//                         <tr>
//                             <th>Item Code</th>
//                             <th>Company</th>
//                             <th>Warehouse</th>
//                             <th>Available Qty</th>
//                         </tr>
//                     </thead>
//                     <tbody id="stock-body">
//                         <tr>
//                             <td colspan="4" style="text-align:center;">Loading...</td>
//                         </tr>
//                     </tbody>
//                 </table>
//             `;

//             d.fields_dict.stock_table.$wrapper.html(html);
//             d.show();

//             let rows = "";
//             let completed = 0;

//             selected_items.forEach(row_name => {

//                 let item = frm.doc.table_feob.find(i => i.name === row_name);
//                 if (!item) return;

//                 // 🔥 IMPORTANT: Get all warehouse stock
//                 frappe.call({
//                     method: "frappe.client.get_list",
//                     args: {
//                         doctype: "Bin",
//                         filters: {
//                             item_code: item.item_code
//                         },
//                         fields: ["warehouse", "actual_qty"]
//                     },
//                     callback: function(r) {

//                         if (r.message && r.message.length > 0) {

//                             r.message.forEach(bin => {

//                                 if (bin.actual_qty > 0) {

//                                     rows += `
//                                         <tr>
//                                             <td>${item.item_code}</td>
//                                             <td>${frm.doc.company}</td>
//                                             <td>${bin.warehouse}</td>
//                                             <td style="color:${bin.actual_qty < 10 ? 'red' : 'green'}">
//                                                 ${bin.actual_qty}
//                                             </td>
//                                         </tr>
//                                     `;
//                                 }

//                             });

//                         }

//                         completed++;

//                         if (completed === selected_items.length) {

//                             d.fields_dict.stock_table.$wrapper
//                                 .find("#stock-body")
//                                 .html(
//                                     rows || `<tr><td colspan="4" style="text-align:center;">No Stock Available</td></tr>`
//                                 );
//                         }
//                     }
//                 });

//             });

//         });

//     }
// }

// // 🔥 PURPOSE BUTTON FINAL (CORRECTED)



// frappe.ui.form.on('Material Indent', {
//     refresh: function(frm) {

//         // ❌ REMOVE THIS (ye issue ka main reason hai)
//         // frm.page.clear_actions_menu();

//         // ==============================
//         // 🔥 MATERIAL ISSUE (POPUP)
//         // ==============================
//         frm.page.add_action_item(__('Material Issue'), function() {

//             let rows = frm.doc.table_feob || [];

//             if (!rows.length) {
//                 frappe.msgprint("❌ Please add items first");
//                 return;
//             }

//             let d = new frappe.ui.Dialog({
//                 title: 'Enter Issue Qty',
//                 size: 'large',
//                 fields: rows.map(row => ({
//                     fieldtype: 'Float',
//                     label: `${row.item_code} (Bal: ${row.custom_qty_balanced || 0})`,
//                     fieldname: row.name,
//                     default: 0
//                 })),
//                 primary_action_label: 'Create Stock Entry',
//                 primary_action(values) {

//                     let items = [];
//                     let promises = [];

//                     rows.forEach(row => {

//                         let qty = values[row.name] || 0;
//                         if (qty <= 0) return;

//                         let p = frappe.db.get_value("Bin", {
//                             item_code: row.item_code,
//                             warehouse: row.from_warehouse
//                         }, "actual_qty").then(r => {

//                             let stock = r.message?.actual_qty || 0;

//                             if (qty > stock) {
//                                 frappe.throw(`❌ Stock not available for ${row.item_code} (Available: ${stock})`);
//                             }

//                             if (qty > (row.custom_qty_balanced || 0)) {
//                                 frappe.throw(`❌ Issue qty exceeds balance for ${row.item_code}`);
//                             }

//                             items.push({
//                                 item_code: row.item_code,
//                                 qty: qty,
//                                 s_warehouse: row.from_warehouse,

//                                 custom_material_indent: frm.doc.name,
//                                 custom_material_indent_item: row.name ,
//                                    custom_specification:row.custom_specification
//                             });

//                         });

//                         promises.push(p);
//                     });

//                     Promise.all(promises).then(() => {

//                         if (!items.length) {
//                             frappe.msgprint("❌ Enter qty first");
//                             return;
//                         }

//                         frappe.call({
//                             method: "frappe.client.insert",
//                             args: {
//                                 doc: {
//                                     doctype: "Stock Entry",
//                                     stock_entry_type: "Material Issue",
//                                     company: frm.doc.company,
//                                     items: items,
//                                      // ✅ ADD THESE
//             custom_username: frm.doc.custom_username,
//             custom_remark: frm.doc.custom_remark,
//             custom_attachment: frm.doc.custome_attachment,
//              custom_design: frm.doc.custom_design,
//                                 }
//                             },
//                             callback: function(r) {
//                                 if (r.message) {
//                                     frappe.show_alert("✅ Stock Entry Created");
//                                     frappe.set_route("Form", "Stock Entry", r.message.name);
//                                 }
//                             }
//                         });

//                         d.hide();
//                     });
//                 }
//             });

//             d.show();
//         });


//         // ==============================
//         // 🔥 MATERIAL PURCHASE (POPUP)
//         // ==============================
//         frm.page.add_action_item(__('Material Purchase'), function() {

//             let rows = frm.doc.table_feob || [];

//             let d = new frappe.ui.Dialog({
//                 title: 'Enter Purchase Qty',
//                 size: 'large',
//                 fields: rows.map(row => ({
//                     fieldtype: 'Float',
//                     label: `${row.item_code} (Bal: ${row.custom_qty_balanced || 0})`,
//                     fieldname: row.name,
//                     default: 0
//                 })),
//                 primary_action_label: 'Create Purchase Request',
//                 primary_action(values) {

//                     let items = [];

//                     rows.forEach(row => {

//                         let qty = values[row.name] || 0;
//                         if (qty <= 0) return;

//                         if (qty > (row.custom_qty_balanced || 0)) {
//                             frappe.throw(`❌ Purchase qty exceeds balance for ${row.item_code}`);
//                         }

//                         items.push({
//                             item_code: row.item_code,
//                             qty: qty,
//                             schedule_date: frm.doc.required_by,
//                             uom: row.uom,

//                             custom_material_indent: frm.doc.name,
//                             custom_material_indent_item: row.name,
//                              custom_specification:row.custom_specification
//                         });
//                     });

//                     if (!items.length) {
//                         frappe.msgprint("❌ Enter qty first");
//                         return;
//                     }

//                     frappe.call({
//                         method: "frappe.client.insert",
//                         args: {
//                             doc: {
//                                 doctype: "Material Request",
//                                 material_request_type: "Purchase",
//                                 company: frm.doc.company,
//                                 items: items,
//                                    // ✅ ADD THESE
//             custom_username: frm.doc.custom_username,
//             custom_remark: frm.doc.custom_remark,
//             custom_attachment: frm.doc.custome_attachment,
//              custom_design: frm.doc.custom_design,
//                             }
//                         },
//                         callback: function(r) {
//                             if (r.message) {
//                                 frappe.show_alert("✅ Purchase Request Created");
//                                 frappe.set_route("Form", "Material Request", r.message.name);
//                             }
//                         }
//                     });

//                     d.hide();
//                 }
//             });

//             d.show();
//         });

//     }
// });



// // ==============================
// // 🔥 READ ONLY FIELDS
// // ==============================
// frappe.ui.form.on('Material Indent', {
//     refresh: function(frm) {

//         frm.fields_dict.table_feob.grid.update_docfield_property(
//             'custom_purchase_qty',
//             'read_only',
//             1
//         );

//         frm.fields_dict.table_feob.grid.update_docfield_property(
//             'custom_issue_qty',
//             'read_only',
//             1
//         );
//     }
// });


// // ==============================
// // 🔥 CALCULATION LOGIC
// // ==============================
// frappe.ui.form.on('Material Request Item', {

//     qty: function(frm, cdt, cdn) {
//         calculate_remaining(frm, cdt, cdn);
//     },

//     custom_purchase_qty: function(frm, cdt, cdn) {
//         calculate_remaining(frm, cdt, cdn);
//     },

//     custom_issue_qty: function(frm, cdt, cdn) {
//         calculate_remaining(frm, cdt, cdn);
//     }
// });

// function calculate_remaining(frm, cdt, cdn) {

//     let row = locals[cdt][cdn];

//     let total = flt(row.qty);
//     let purchase = flt(row.custom_purchase_qty);
//     let issue = flt(row.custom_issue_qty);

//     let remaining = total - purchase - issue;

//     if (remaining < 0) {
//         frappe.msgprint(`❌ Balance negative for ${row.item_code}`);
//         remaining = 0;
//     }

//     row.custom_qty_balanced = remaining;

//     frm.refresh_field('table_feob');
// }


// // ==============================
// // 🔥 REFRESH CALCULATION
// // ==============================
// frappe.ui.form.on('Material Indent', {
//     refresh: function(frm) {

//         (frm.doc.table_feob || []).forEach(row => {

//             let total = flt(row.qty);
//             let purchase = flt(row.custom_purchase_qty);
//             let issue = flt(row.custom_issue_qty);

//             row.custom_qty_balanced = total - purchase - issue;

//             if (row.custom_qty_balanced < 0) {
//                 row.custom_qty_balanced = 0;
//             }
//         });

//         frm.refresh_field('table_feob');
//     }
// });



