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

        if item.material_indent and item.material_indent_item:

            indent = frappe.get_doc("Material Indent", item.material_indent)

            for row in indent.table_feob:

                if row.name == item.material_indent_item:

                    remaining = (row.qty or 0) - (row.purchased_qty or 0)

                    # 🔥 VALIDATION
                    if item.purchased_qty and item.purchased_qty > remaining:
                        frappe.throw(f"❌ Purchase qty cannot be greater than remaining qty for {row.item_code}")
def update_purchase(doc, method):

    for item in doc.items:

        if item.material_indent and item.material_indent_item:

            indent = frappe.get_doc("Material Indent", item.material_indent)

            for row in indent.table_feob:

                if row.name == item.material_indent_item:

                    purchased = item.purchased_qty or 0

                    # 🔥 SAFE VALIDATION AGAIN
                    remaining = (row.qty or 0) - (row.purchased_qty or 0)

                    if purchased > remaining:
                        frappe.throw(f"❌ Cannot purchase more than remaining qty for {row.item_code}")

                    row.purchased_qty = (row.purchased_qty or 0) + purchased

                    row.remaining_qty = (row.qty or 0) - row.purchased_qty - (row.issued_qty or 0)

            indent.save(ignore_permissions=True)






def validate_stock_entry(doc, method):

    for item in doc.items:

        if item.material_indent and item.material_indent_item:

            indent = frappe.get_doc("Material Indent", item.material_indent)

            for row in indent.table_feob:

                if row.name == item.material_indent_item:

                    remaining = (row.qty or 0) - (row.purchased_qty or 0) - (row.issued_qty or 0)

                    # 🔥 VALIDATION
                    if item.issue_qty and item.issue_qty > remaining:
                        frappe.throw(f"❌ Issue qty cannot be greater than remaining qty for {row.item_code}")

def update_issue(doc, method):

    for item in doc.items:

        if item.material_indent and item.material_indent_item:

            indent = frappe.get_doc("Material Indent", item.material_indent)

            for row in indent.table_feob:

                if row.name == item.material_indent_item:

                    issued = item.issue_qty or 0

                    # 🔥 SAFE VALIDATION AGAIN
                    remaining = (row.qty or 0) - (row.purchased_qty or 0) - (row.issued_qty or 0)

                    if issued > remaining:
                        frappe.throw(f"❌ Cannot issue more than remaining qty for {row.item_code}")

                    row.issued_qty = (row.issued_qty or 0) + issued

                    row.remaining_qty = (row.qty or 0) - (row.purchased_qty or 0) - row.issued_qty

            indent.save(ignore_permissions=True)














# import frappe
# from frappe.model.document import Document

# class MaterialIndent(Document):
#     pass


# def validate_material_request(doc, method):

#     for item in doc.items:

#         if item.material_indent and item.material_indent_item:

#             indent = frappe.get_doc("Material Indent", item.material_indent)

#             for row in indent.table_feob:

#                 if row.name == item.material_indent_item:

#                     remaining = (row.qty or 0) - (row.purchased_qty or 0)

#                     # 🔥 VALIDATION
#                     if item.purchased_qty and item.purchased_qty > remaining:
#                         frappe.throw(f"❌ Purchase qty cannot be greater than remaining qty for {row.item_code}")
# def update_purchase(doc, method):

#     for item in doc.items:

#         if item.material_indent and item.material_indent_item:

#             indent = frappe.get_doc("Material Indent", item.material_indent)

#             for row in indent.table_feob:

#                 if row.name == item.material_indent_item:

#                     purchased = item.purchased_qty or 0

#                     # 🔥 SAFE VALIDATION AGAIN
#                     remaining = (row.qty or 0) - (row.purchased_qty or 0)

#                     if purchased > remaining:
#                         frappe.throw(f"❌ Cannot purchase more than remaining qty for {row.item_code}")

#                     row.purchased_qty = (row.purchased_qty or 0) + purchased

#                     row.remaining_qty = (row.qty or 0) - row.purchased_qty - (row.issued_qty or 0)

#             indent.save(ignore_permissions=True)






# def validate_stock_entry(doc, method):

#     for item in doc.items:

#         if item.material_indent and item.material_indent_item:

#             indent = frappe.get_doc("Material Indent", item.material_indent)

#             for row in indent.table_feob:

#                 if row.name == item.material_indent_item:

#                     remaining = (row.qty or 0) - (row.purchased_qty or 0) - (row.issued_qty or 0)

#                     # 🔥 VALIDATION
#                     if item.issue_qty and item.issue_qty > remaining:
#                         frappe.throw(f"❌ Issue qty cannot be greater than remaining qty for {row.item_code}")

# def update_issue(doc, method):

#     for item in doc.items:

#         if item.material_indent and item.material_indent_item:

#             indent = frappe.get_doc("Material Indent", item.material_indent)

#             for row in indent.table_feob:

#                 if row.name == item.material_indent_item:

#                     issued = item.issue_qty or 0

#                     # 🔥 SAFE VALIDATION AGAIN
#                     remaining = (row.qty or 0) - (row.purchased_qty or 0) - (row.issued_qty or 0)

#                     if issued > remaining:
#                         frappe.throw(f"❌ Cannot issue more than remaining qty for {row.item_code}")

#                     row.issued_qty = (row.issued_qty or 0) + issued

#                     row.remaining_qty = (row.qty or 0) - (row.purchased_qty or 0) - row.issued_qty

#             indent.save(ignore_permissions=True)


