app_name = "material_indent"
app_title = "Material Indent"
app_publisher = "shubhangi pawar"
app_description = "Material Indent"
app_email = "shubhangipawar7225@gmail.com"
app_license = "mit"


doc_events = {
    "Material Request": {
        "validate": "material_indent.material_indent.doctype.material_indent.material_indent.validate_material_request",
        "on_submit": "material_indent.material_indent.doctype.material_indent.material_indent.update_purchase"
    },
    "Stock Entry": {
        "validate": "material_indent.material_indent.doctype.material_indent.material_indent.validate_stock_entry",
        "on_submit": "material_indent.material_indent.doctype.material_indent.material_indent.update_issue"
    }
}





fixtures = [

    # =====================================================
    # CUSTOM FIELD
    # =====================================================
    {
        "doctype": "Custom Field",
        "filters": [
            ["name", "in", [

                # ---------------------------------
                # Material Indent
                # ---------------------------------
                "Material Indent-custom_indent_status",
                "Material Indent-custom_closed_by_user_",
                "Material Indent-custom_material_purchase",
                "Material Indent-custom_material_issue",
                "Material Indent-custom_status",
                "Material Indent-custom_info",
                "Material Indent-custom_stock_entries",
                "Material Indent-custom_column_break_xemhe",
                "Material Indent-custom_material_requests",
                "Material Indent-custom_section_break_kwgez",

                # ---------------------------------
                # Material Request (Parent)
                # ---------------------------------
                "Material Request-custom_material_indent",
                "Material Request-custom_activity_timeline_json",
                "Material Request-custom_activity_timeline",
                "Material Request-custom_section_break_u5yuw",
                "Material Request-custom_custom_activity_logs",
                "Material Request-custom_workflow_status",
                "Material Request-custom_department",
                "Material Request-custom_category",
                "Material Request-custom_select_project_",
                "Material Request-custom_design",
                "Material Request-custom_attachment",
                "Material Request-custom_remark",
                "Material Request-custom_username",

                # ---------------------------------
                # Material Request Item (Child)
                # ---------------------------------
                "Material Request Item-custom_material_indent_item",
                "Material Request Item-custom_material_indent",
                "Material Request Item-custom_specification",
                "Material Request Item-custom_qty_balanced",
                "Material Request Item-custom_issue_qty",
                "Material Request Item-custom_purchase_qty",

                # ---------------------------------
                # Stock Entry (Parent)
                # ---------------------------------
                "Stock Entry-custom_material_indent",
                "Stock Entry-custom_department",
                "Stock Entry-custom_design",
                "Stock Entry-custom_attachment",
                "Stock Entry-custom_remark",
                "Stock Entry-custom_username",

                # ---------------------------------
                # Stock Entry Detail (Child)
                # ---------------------------------
                "Stock Entry Detail-custom_qty_balanced",
                "Stock Entry Detail-custom_specification",
                "Stock Entry Detail-custom_material_indent_item",
                "Stock Entry Detail-custom_material_indent",
                "Stock Entry Detail-custom_issue_qty",

                # ---------------------------------
                # Purchase Order
                # ---------------------------------
                "Purchase Order-custom_approved_by_signature",
                "Purchase Order-custom_category",
                "Purchase Order-custom_remark",
                "Purchase Order-custom_project_name",

                # ---------------------------------
                # Purchase Order Item
                # ---------------------------------
                "Purchase Order Item-custom_specification"

            ]]
        ]
    },

    # =====================================================
    # CLIENT SCRIPT
    # =====================================================
    {
        "doctype": "Client Script",
        "filters": [
            ["dt", "in", [
                "Material Indent",
                "Material Request",
                "Stock Entry",
                "Purchase Order"
            ]]
        ]
    },

    # =====================================================
    # SERVER SCRIPT
    # =====================================================
    {
        "doctype": "Server Script",
        "filters": [
            ["module", "in", [
                "commit",
                "Material Indent"
            ]]
        ]
    }
]













# fixtures = [
#     {
#         "doctype": "Custom Field",
#         "filters": [
#             ["name", "in", [
#                 # 🔹 Parent - Material Request
#                 "Material Request-custom_attachment",
#                 "Material Request-custom_remark",
#                 "Material Request-custom_username",

#                 # 🔹 Parent - Stock Entry
#                 "Stock Entry-custom_attachment",
#                 "Stock Entry-custom_remark",
#                 "Stock Entry-custom_username",

#                 # 🔹 Child - Stock Entry Detail
#                 "Stock Entry Detail-custom_specification",
#                 "Stock Entry Detail-custom_material_indent_item",
#                 "Stock Entry Detail-custom_material_indent",
#                 "Stock Entry Detail-custom_issue_qty",

#                 # 🔹 Child - Material Request Item
#                 "Material Request Item-custom_material_indent_item",
#                 "Material Request Item-custom_material_indent",
#                 "Material Request Item-custom_specification",
#                 "Material Request Item-custom_qty_balanced",
#                 "Material Request Item-custom_issue_qty",
#                 "Material Request Item-custom_purchase_qty"
#             ]]
#         ]
#     }
# ]





# fixtures = [
#     {
#         "dt": "Custom Field",
#         "filters": [
#             ["name", "in", [

#                 # Material Request Item
#                 "Material Request Item-purchased_qty",
#                 "Material Request Item-remaining_qty",
#                 "Material Request Item-issued_qty",
#                 "Material Request Item-specification",
#                 "Material Request Item-material_indent",
#                 "Material Request Item-material_indent_item",

#                 # Stock Entry Detail
#                 "Stock Entry Detail-material_indent",
#                 "Stock Entry Detail-material_indent_item",
#                 "Stock Entry Detail-issue_qty",

#                 # Material Request
#                 "Material Request-user",
#                 "Material Request-remark",

#                 # Stock Entry
#                 "Stock Entry-user",
#                 "Stock Entry-remark"

#             ]]
#         ]
#     }
# ]


# doc_events = {
#     "Material Request": {
#         "on_submit": "material_indent.material_indent.doctype.material_indent.material_indent.update_purchase"
#     },
#    "Stock Entry": {
#         "on_submit": "material_indent.material_indent.doctype.material_indent.material_indent.update_issue"
#     }
# }
# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "material_indent",
# 		"logo": "/assets/material_indent/logo.png",
# 		"title": "Material Indent",
# 		"route": "/material_indent",
# 		"has_permission": "material_indent.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/material_indent/css/material_indent.css"
# app_include_js = "/assets/material_indent/js/material_indent.js"

# include js, css files in header of web template
# web_include_css = "/assets/material_indent/css/material_indent.css"
# web_include_js = "/assets/material_indent/js/material_indent.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "material_indent/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "material_indent/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "material_indent.utils.jinja_methods",
# 	"filters": "material_indent.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "material_indent.install.before_install"
# after_install = "material_indent.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "material_indent.uninstall.before_uninstall"
# after_uninstall = "material_indent.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "material_indent.utils.before_app_install"
# after_app_install = "material_indent.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "material_indent.utils.before_app_uninstall"
# after_app_uninstall = "material_indent.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "material_indent.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"material_indent.tasks.all"
# 	],
# 	"daily": [
# 		"material_indent.tasks.daily"
# 	],
# 	"hourly": [
# 		"material_indent.tasks.hourly"
# 	],
# 	"weekly": [
# 		"material_indent.tasks.weekly"
# 	],
# 	"monthly": [
# 		"material_indent.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "material_indent.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "material_indent.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "material_indent.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["material_indent.utils.before_request"]
# after_request = ["material_indent.utils.after_request"]

# Job Events
# ----------
# before_job = ["material_indent.utils.before_job"]
# after_job = ["material_indent.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"material_indent.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

