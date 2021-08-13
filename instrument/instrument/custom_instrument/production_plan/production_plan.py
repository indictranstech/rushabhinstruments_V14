from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

@frappe.whitelist()
def on_update(doc,method):
	ohs = get_current_stock()
	if doc.sub_assembly_items:
		for row in doc.sub_assembly_items:
			if row.production_item in ohs:
				req_qty = row.qty
				row.available_quantity = ohs.get(row.production_item)
				row.calculated_required_quantity = abs(req_qty - ohs.get(row.production_item)) if req_qty > ohs.get(row.production_item) else 0
				row.qty = row.calculated_required_quantity

@frappe.whitelist()
def validate(doc,method):
	ohs = get_current_stock()
	if doc.po_items:
		for row in doc.po_items:
			if row.item_code in ohs:
				row.available_quantity = ohs.get(row.item_code)
				# frappe.db.set_value("Work Order",doc.name,'available_quantity',ohs.get(row.item_code))
				# frappe.db.commit()
				# doc.reload()

def get_current_stock():
	# 1.get wip warehouse
	wip_warehouse = frappe.db.get_single_value("Manufacturing Settings", 'default_wip_warehouse')
	current_stock = frappe.db.sql("""SELECT item_code,sum(actual_qty) as qty from `tabBin` where warehouse != '{0}' group by item_code """.format(wip_warehouse),as_dict=1)
	ohs_dict = {item.item_code : item.qty for item in current_stock}
	return ohs_dict