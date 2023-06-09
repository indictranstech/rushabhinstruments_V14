# Copyright (c) 2022, instrument and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	data = []
	columns = get_columns()
	data = get_data(filters)
	return columns, data
def get_data(filters):
	data = frappe.db.sql("""SELECT bi.item_code as item,b.name as reference_bom,bi.bom_no ,i.default_bom from `tabBOM Item` bi join `tabBOM` b on b.name = bi.parent join `tabItem` i on i.item_code = bi.item_code where i.default_bom != bi.bom_no""",as_dict=1)
	data1 = frappe.db.sql("""SELECT bi.is_map_item,bi.item_code as item,b.name as reference_mapped_bom,bi.mapped_bom  from `tabMapped BOM Item` bi join `tabMapped BOM` b on b.name = bi.parent join `tabItem` i on i.item_code = bi.item_code where i.default_bom != bi.bom_no""",as_dict=1)
	if data1:
		for row in data1:
			if row.is_map_item:
				default_mapped_bom = frappe.db.get_value("Mapped BOM",{'item':row.item,'is_active':1,'is_default':1},'name')
				row['default_mapped_bom'] = default_mapped_bom
			data.append(row)
	# data = frappe.db.sql("""SELECT bi.item_code as item ,i.default_bom as bom_with_item_in_item_list ,bi.bom_no from `tabBOM` b join `tabBOM Item` bi on bi.parent = b.name join `tabItem` i on bi.item_code = i.item_code""",as_dict=1,debug=1)
	return data
def get_columns():
	return [
		{
			"label": " Standard Item",
			"fieldtype": "Link",
			"fieldname": "item",
			"options":"Item",
			"width": 300
		},
		# {
		# 	"label": " Mapped Item",
		# 	"fieldtype": "Link",
		# 	"fieldname": "mapped_item",
		# 	"options":"Item",
		# 	"width": 300
		# },
		{
			"label": "Reference BOM",
			"fieldtype": "Link",
			"fieldname": "reference_bom",
			"options":"BOM",
			"width": 300
		},
		{
			"label": "Reference Mapped BOM",
			"fieldtype": "Link",
			"fieldname": "reference_mapped_bom",
			"options":"BOM",
			"width": 300
		},
		{
			"label": "BOM No",
			"fieldtype": "Link",
			"fieldname": "bom_no",
			"options":"BOM",
			"width": 300
		},
		{
			"label": " Mapped BOM No",
			"fieldtype": "Link",
			"fieldname": "mapped_bom_no",
			"options":"BOM",
			"width": 300
		},
		# {
		# 	"label": "BOM with Item in Item List",
		# 	"fieldtype": "Link",
		# 	"fieldname": "bom_with_item_in_item_list",
		# 	"options":"BOM",
		# 	"width": 150
		# },
		# {
		# 	"label": "Mapped BOM with Item in Item List",
		# 	"fieldtype": "Link",
		# 	"fieldname": "mapped_bom_with_item_in_item_list",
		# 	"options":"Mapped BOM",
		# 	"width": 150
		# },
		# {
		# 	"label": "Reference BOM in Item list",
		# 	"fieldtype": "Link",
		# 	"fieldname": "reference_bom_in_item_list",
		# 	"options":"BOM",
		# 	"width": 150
		# },
		{
			"label": "Default BOM",
			"fieldtype": "Link",
			"fieldname": "default_bom",
			"options":"BOM",
			"width": 150
		},
		{
			"label": "Default Mapped BOM",
			"fieldtype": "Link",
			"fieldname": "default_mapped_bom",
			"options":"BOM",
			"width": 150
		},
		# {
		# 	"label": "Reference Mapped BOM Item list",
		# 	"fieldtype": "Link",
		# 	"fieldname": "reference_mapped_bom_in_item_list",
		# 	"options":"Mapped BOM",
		# 	"width": 150
		# },
		# {
		# 	"label": "Default Mapped BOM",
		# 	"fieldtype": "Link",
		# 	"fieldname": "default_mapped_bom",
		# 	"options":"Mapped BOM",
		# 	"width": 150
		# }

	]
def get_conditions(filters=None):
	conditions = "1=1 "
	if filters.get("project") :
		conditions += "and project = '{0}'".format(filters.get("project"))
	if filters.get("subject") :
		conditions += "and subject like '{0}'".format(filters.get("subject"))
	if filters.get("status") :
		conditions += " and status = '{0}' ".format(filters.get("status"))
	if filters.get("task") :
		conditions += " and name = '{0}' ".format(filters.get("task"))
	if filters.get("priority"):
		conditions += " and priority like '{0}'".format(filters.get('priority'))
		
	return conditions
