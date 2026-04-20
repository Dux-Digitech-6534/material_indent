# Copyright (c) 2026, shubhangi pawar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MaterialIndent(Document):
	pass



def validate_material_request(doc, method):

    for item in doc.items:

        if not (item.custom_material_indent and item.custom_material_indent_item):
            continue

        indent = frappe.get_doc("Material Indent", item.custom_material_indent)

        for row in indent.table_feob:

            if row.name == item.custom_material_indent_item:

                purchase_qty = item.qty or 0

                # ✅ ONLY ISSUE BASED (purchase ignore)
                remaining = (row.qty or 0) - (row.custom_issue_qty or 0)

                # 👉 अगर purchase limit नहीं चाहिए तो नीचे वाला if हटा दे
                # if purchase_qty > remaining:
                #     frappe.throw(f"❌ Purchase qty cannot be greater than required qty for {row.item_code}")

def update_purchase(doc, method):

    for item in doc.items:

        if not (item.custom_material_indent and item.custom_material_indent_item):
            continue

        indent = frappe.get_doc("Material Indent", item.custom_material_indent)

        for row in indent.table_feob:

            if row.name == item.custom_material_indent_item:

                purchase_qty = item.qty or 0

                # ✅ UPDATE PURCHASE
                row.custom_purchase_qty = (row.custom_purchase_qty or 0) + purchase_qty

                # 🔥 FIX: balance ONLY issue से
                row.custom_qty_balanced = (row.qty or 0) - (row.custom_issue_qty or 0)

        indent.save(ignore_permissions=True)

def validate_stock_entry(doc, method):

    for item in doc.items:

        if not (item.custom_material_indent and item.custom_material_indent_item):
            continue

        indent = frappe.get_doc("Material Indent", item.custom_material_indent)

        for row in indent.table_feob:

            if row.name == item.custom_material_indent_item:

                issue_qty = item.qty or 0

                # 🔥 FIX: purchase ignore
                remaining = (row.qty or 0) - (row.custom_issue_qty or 0)

                if issue_qty > remaining:
                    frappe.throw(f"❌ Issue qty cannot be greater than required qty for {row.item_code}")

def update_issue(doc, method):

    for item in doc.items:

        if not (item.custom_material_indent and item.custom_material_indent_item):
            continue

        indent = frappe.get_doc("Material Indent", item.custom_material_indent)

        for row in indent.table_feob:

            if row.name == item.custom_material_indent_item:

                issue_qty = item.qty or 0

                # ✅ UPDATE ISSUE
                row.custom_issue_qty = (row.custom_issue_qty or 0) + issue_qty

                # 🔥 FIX
                row.custom_qty_balanced = (row.qty or 0) - row.custom_issue_qty

        indent.save(ignore_permissions=True)














# import frappe
# from frappe.model.document import Document

# class MaterialIndent(Document):
#     pass

# def validate_material_request(doc, method):

#     for item in doc.items:

#         if not (item.custom_material_indent and item.custom_material_indent_item):
#             continue

#         indent = frappe.get_doc("Material Indent", item.custom_material_indent)

#         for row in indent.table_feob:

#             if row.name == item.custom_material_indent_item:

#                 purchase_qty = item.qty or 0   # ✅ ERP QTY

#                 remaining = (row.qty or 0) \
#                             - (row.custom_purchase_qty or 0) \
#                             - (row.custom_issue_qty or 0)

#                 if purchase_qty > remaining:
#                     frappe.throw(f"❌ Purchase qty cannot be greater than remaining qty for {row.item_code}")


# def update_purchase(doc, method):

#     for item in doc.items:

#         if not (item.custom_material_indent and item.custom_material_indent_item):
#             continue

#         indent = frappe.get_doc("Material Indent", item.custom_material_indent)

#         updated = False

#         for row in indent.table_feob:

#             if row.name == item.custom_material_indent_item:

#                 purchase_qty = item.qty or 0   # ✅ ERP QTY

#                 remaining = (row.qty or 0) \
#                             - (row.custom_purchase_qty or 0) \
#                             - (row.custom_issue_qty or 0)

#                 if purchase_qty > remaining:
#                     frappe.throw(f"❌ Cannot purchase more than remaining qty for {row.item_code}")

#                 # ✅ UPDATE PURCHASE
#                 row.custom_purchase_qty = (row.custom_purchase_qty or 0) + purchase_qty

#                 # ✅ UPDATE BALANCE
#                 row.custom_qty_balanced = (row.qty or 0) \
#                                         - row.custom_purchase_qty \
#                                         - (row.custom_issue_qty or 0)

#                 updated = True

#         if updated:
#             indent.save(ignore_permissions=True)        



# def validate_stock_entry(doc, method):

#     for item in doc.items:

#         if not (item.custom_material_indent and item.custom_material_indent_item):
#             continue

#         indent = frappe.get_doc("Material Indent", item.custom_material_indent)

#         for row in indent.table_feob:

#             if row.name == item.custom_material_indent_item:

#                 issue_qty = item.qty or 0   # ✅ ERP QTY

#                 remaining = (row.qty or 0) \
#                             - (row.custom_purchase_qty or 0) \
#                             - (row.custom_issue_qty or 0)

#                 if issue_qty > remaining:
#                     frappe.throw(f"❌ Issue qty cannot be greater than remaining qty for {row.item_code}")                        


# def update_issue(doc, method):

#     for item in doc.items:

#         if not (item.custom_material_indent and item.custom_material_indent_item):
#             continue

#         indent = frappe.get_doc("Material Indent", item.custom_material_indent)

#         updated = False

#         for row in indent.table_feob:

#             if row.name == item.custom_material_indent_item:

#                 issue_qty = item.qty or 0   # ✅ ERP QTY

#                 remaining = (row.qty or 0) \
#                             - (row.custom_purchase_qty or 0) \
#                             - (row.custom_issue_qty or 0)

#                 if issue_qty > remaining:
#                     frappe.throw(f"❌ Cannot issue more than remaining qty for {row.item_code}")

#                 # ✅ UPDATE ISSUE
#                 row.custom_issue_qty = (row.custom_issue_qty or 0) + issue_qty

#                 # ✅ UPDATE BALANCE
#                 row.custom_qty_balanced = (row.qty or 0) \
#                                         - (row.custom_purchase_qty or 0) \
#                                         - row.custom_issue_qty

#                 updated = True

#         if updated:
#             indent.save(ignore_permissions=True)












