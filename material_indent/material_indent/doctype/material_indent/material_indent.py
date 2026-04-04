# Copyright (c) 2026, shubhangi pawar and contributors
# For license information, please see license.txt

# import frappe
# from frappe.model.document import Document


# class MaterialIndent(Document):
# 	pass



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

                purchase_qty = item.qty or 0   # ✅ ERP QTY

                remaining = (row.qty or 0) \
                            - (row.custom_purchase_qty or 0) \
                            - (row.custom_issue_qty or 0)

                if purchase_qty > remaining:
                    frappe.throw(f"❌ Purchase qty cannot be greater than remaining qty for {row.item_code}")


def update_purchase(doc, method):

    for item in doc.items:

        if not (item.custom_material_indent and item.custom_material_indent_item):
            continue

        indent = frappe.get_doc("Material Indent", item.custom_material_indent)

        updated = False

        for row in indent.table_feob:

            if row.name == item.custom_material_indent_item:

                purchase_qty = item.qty or 0   # ✅ ERP QTY

                remaining = (row.qty or 0) \
                            - (row.custom_purchase_qty or 0) \
                            - (row.custom_issue_qty or 0)

                if purchase_qty > remaining:
                    frappe.throw(f"❌ Cannot purchase more than remaining qty for {row.item_code}")

                # ✅ UPDATE PURCHASE
                row.custom_purchase_qty = (row.custom_purchase_qty or 0) + purchase_qty

                # ✅ UPDATE BALANCE
                row.custom_qty_balanced = (row.qty or 0) \
                                        - row.custom_purchase_qty \
                                        - (row.custom_issue_qty or 0)

                updated = True

        if updated:
            indent.save(ignore_permissions=True)        



def validate_stock_entry(doc, method):

    for item in doc.items:

        if not (item.custom_material_indent and item.custom_material_indent_item):
            continue

        indent = frappe.get_doc("Material Indent", item.custom_material_indent)

        for row in indent.table_feob:

            if row.name == item.custom_material_indent_item:

                issue_qty = item.qty or 0   # ✅ ERP QTY

                remaining = (row.qty or 0) \
                            - (row.custom_purchase_qty or 0) \
                            - (row.custom_issue_qty or 0)

                if issue_qty > remaining:
                    frappe.throw(f"❌ Issue qty cannot be greater than remaining qty for {row.item_code}")                        


def update_issue(doc, method):

    for item in doc.items:

        if not (item.custom_material_indent and item.custom_material_indent_item):
            continue

        indent = frappe.get_doc("Material Indent", item.custom_material_indent)

        updated = False

        for row in indent.table_feob:

            if row.name == item.custom_material_indent_item:

                issue_qty = item.qty or 0   # ✅ ERP QTY

                remaining = (row.qty or 0) \
                            - (row.custom_purchase_qty or 0) \
                            - (row.custom_issue_qty or 0)

                if issue_qty > remaining:
                    frappe.throw(f"❌ Cannot issue more than remaining qty for {row.item_code}")

                # ✅ UPDATE ISSUE
                row.custom_issue_qty = (row.custom_issue_qty or 0) + issue_qty

                # ✅ UPDATE BALANCE
                row.custom_qty_balanced = (row.qty or 0) \
                                        - (row.custom_purchase_qty or 0) \
                                        - row.custom_issue_qty

                updated = True

        if updated:
            indent.save(ignore_permissions=True)














# def validate_material_request(doc, method):

#     for item in doc.items:

#         if item.custom_material_indent and item.custom_material_indent_item:

#             indent = frappe.get_doc("Material Indent", item.custom_material_indent)

#             for row in indent.table_feob:

#                 if row.name == item.custom_material_indent_item:

#                     remaining = (row.qty or 0) - (row.custom_purchase_qty or 0)

#                     # 🔥 VALIDATION
#                     if item.custom_purchase_qty and item.custom_purchase_qty > remaining:
#                         frappe.throw(f"❌ Purchase qty cannot be greater than remaining qty for {row.item_code}")
# def update_purchase(doc, method):

#     for item in doc.items:

#         if item.custom_material_indent and item.custom_material_indent_item:

#             indent = frappe.get_doc("Material Indent", item.custom_material_indent)

#             for row in indent.table_feob:

#                 if row.name == item.custom_material_indent_item:

#                     purchased = item.custom_purchase_qty or 0

#                     # 🔥 SAFE VALIDATION AGAIN
#                     remaining = (row.qty or 0) - (row.custom_purchase_qty or 0)

#                     if purchased > remaining:
#                         frappe.throw(f"❌ Cannot purchase more than remaining qty for {row.item_code}")

#                     row.custom_purchase_qty = (row.custom_purchase_qty or 0) + purchased

#                     row.custom_qty_balanced = (row.qty or 0) - row.custom_purchase_qty - (row.custom_issue_qty or 0)

#             indent.save(ignore_permissions=True)






# def validate_stock_entry(doc, method):

#     for item in doc.items:

#         if item.custom_material_indent and item.custom_material_indent_item:

#             indent = frappe.get_doc("Material Indent", item.custom_material_indent)

#             for row in indent.table_feob:

#                 if row.name == item.custom_material_indent_item:

#                     remaining = (row.qty or 0) - (row.custom_purchase_qty or 0) - (row.custom_issue_qty or 0)

#                     # 🔥 VALIDATION
#                     if item.custom_issue_qty and item.custom_issue_qty > remaining:
#                         frappe.throw(f"❌ Issue qty cannot be greater than remaining qty for {row.item_code}")

# def update_issue(doc, method):

#     for item in doc.items:

#         if item.custom_material_indent and item.custom_material_indent_item:

#             indent = frappe.get_doc("Material Indent", item.custom_material_indent)

#             for row in indent.table_feob:

#                 if row.name == item.custom_material_indent_item:

#                     issued = item.custom_issue_qty or 0

#                     # 🔥 SAFE VALIDATION AGAIN
#                     remaining = (row.qty or 0) - (row.custom_purchase_qty or 0) - (row.custom_issue_qty or 0)

#                     if issued > remaining:
#                         frappe.throw(f"❌ Cannot issue more than remaining qty for {row.item_code}")

#                     row.custom_issue_qty = (row.custom_issue_qty or 0) + issued

#                     row.custom_qty_balanced = (row.qty or 0) - (row.custom_purchase_qty or 0) - row.custom_issue_qty

#             indent.save(ignore_permissions=True)














# import frappe
# from frappe.model.document import Document

# class MaterialIndent(Document):
#     pass


# def validate_material_request(doc, method):

#     for item in doc.items:

#         if item.custom_material_indent and item.custom_material_indent_item:

#             indent = frappe.get_doc("Material Indent", item.custom_material_indent)

#             for row in indent.table_feob:

#                 if row.name == item.custom_material_indent_item:

#                     remaining = (row.qty or 0) - (row.custom_purchase_qty or 0)

#                     # 🔥 VALIDATION
#                     if item.custom_purchase_qty and item.custom_purchase_qty > remaining:
#                         frappe.throw(f"❌ Purchase qty cannot be greater than remaining qty for {row.item_code}")
# def update_purchase(doc, method):

#     for item in doc.items:

#         if item.custom_material_indent and item.custom_material_indent_item:

#             indent = frappe.get_doc("Material Indent", item.custom_material_indent)

#             for row in indent.table_feob:

#                 if row.name == item.custom_material_indent_item:

#                     purchased = item.custom_purchase_qty or 0

#                     # 🔥 SAFE VALIDATION AGAIN
#                     remaining = (row.qty or 0) - (row.custom_purchase_qty or 0)

#                     if purchased > remaining:
#                         frappe.throw(f"❌ Cannot purchase more than remaining qty for {row.item_code}")

#                     row.custom_purchase_qty = (row.custom_purchase_qty or 0) + purchased

#                     row.custom_qty_balanced = (row.qty or 0) - row.custom_purchase_qty - (row.custom_issue_qty or 0)

#             indent.save(ignore_permissions=True)






# def validate_stock_entry(doc, method):

#     for item in doc.items:

#         if item.custom_material_indent and item.custom_material_indent_item:

#             indent = frappe.get_doc("Material Indent", item.custom_material_indent)

#             for row in indent.table_feob:

#                 if row.name == item.custom_material_indent_item:

#                     remaining = (row.qty or 0) - (row.custom_purchase_qty or 0) - (row.custom_issue_qty or 0)

#                     # 🔥 VALIDATION
#                     if item.issue_qty and item.issue_qty > remaining:
#                         frappe.throw(f"❌ Issue qty cannot be greater than remaining qty for {row.item_code}")

# def update_issue(doc, method):

#     for item in doc.items:

#         if item.custom_material_indent and item.custom_material_indent_item:

#             indent = frappe.get_doc("Material Indent", item.custom_material_indent)

#             for row in indent.table_feob:

#                 if row.name == item.custom_material_indent_item:

#                     issued = item.issue_qty or 0

#                     # 🔥 SAFE VALIDATION AGAIN
#                     remaining = (row.qty or 0) - (row.custom_purchase_qty or 0) - (row.custom_issue_qty or 0)

#                     if issued > remaining:
#                         frappe.throw(f"❌ Cannot issue more than remaining qty for {row.item_code}")

#                     row.custom_issue_qty = (row.custom_issue_qty or 0) + issued

#                     row.custom_qty_balanced = (row.qty or 0) - (row.custom_purchase_qty or 0) - row.custom_issue_qty

#             indent.save(ignore_permissions=True)


