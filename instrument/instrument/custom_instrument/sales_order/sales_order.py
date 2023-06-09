from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


def on_submit(doc, method = None):
	# reminder on submit
	file_att = []
	file_att = [frappe.attach_print(doc.doctype, doc.name, file_name=doc.name)]
	attachments = frappe.db.sql(""" SELECT file_name  FROM tabFile 
				WHERE attached_to_name = '{0}'""".format(doc.name),as_dict=1)
	if attachments:
		for row in attachments:
			_file = frappe.get_doc("File", {"file_name": row.file_name})
			content = _file.get_content()
			if not content:
				return
			attachment_list = {'fname':row.file_name,'fcontent':content}
			file_att.append(attachment_list)
	sender = frappe.db.get_value("Email Setting",{"email_name": "Sales Order Email"},"email_id")
	recipient = doc.contact_email
	if recipient:
		frappe.sendmail(
			sender = sender,
			recipients = recipient,
			subject = "Sales Order : {0}".format(doc.name),
			message = "Sales Order: "+"https://uatrushabhinstruments.indictranstech.com/app/sales-order/{0}".format(doc.name),
			attachments = file_att,
			)

def validate(doc,method):
	if not doc.get("__islocal"):
		start_string = doc.name 
		end_string = '.png'
		label_files = frappe.db.sql("""SELECT file_name from `tabFile` where attached_to_name = '{0}' and attached_to_doctype = 'Sales Order' and file_name like '{1}%{2}'""".format(doc.name,start_string,end_string),as_dict=1)
		if label_files:
			frappe.db.sql("""DELETE from `tabFile` where attached_to_doctype='Sales Order' and attached_to_name=%s and file_name != %s""",
			(doc.name,label_files[0].file_name))
		else:
			frappe.db.sql("""DELETE from `tabFile` where attached_to_doctype='Sales Order' and attached_to_name=%s""",
		(doc.name))
		# frappe.db.sql("""DELETE from `tabFile` where attached_to_doctype='Sales Order' and attached_to_name=%s""",
		# 	(doc.name))
		pdf_data=frappe.attach_print('Sales Order',doc.name, print_format='Sales Order Print')
		
		_file = frappe.get_doc({
		"doctype": "File",
		"file_name": pdf_data.get('fname'),
		"attached_to_doctype": "Sales Order",
		"attached_to_name": doc.name,
		"is_private": 1,
		"content": pdf_data.get('fcontent')
		})
		_file.save()
def after_insert(doc,method):
	start_string = doc.name 
	end_string = '.png'
	label_files = frappe.db.sql("""SELECT file_name from `tabFile` where attached_to_name = '{0}' and attached_to_doctype = 'Sales Order' and file_name like '{1}%{2}'""".format(doc.name,start_string,end_string),as_dict=1)
	if label_files:
		frappe.db.sql("""DELETE from `tabFile` where attached_to_doctype='Sales Order' and attached_to_name=%s and file_name != %s""",
		(doc.name,label_files[0].file_name))
	else:
		frappe.db.sql("""DELETE from `tabFile` where attached_to_doctype='Sales Order' and attached_to_name=%s""",
	(doc.name))
	# frappe.db.sql("""DELETE from `tabFile` where attached_to_doctype='Sales Order' and attached_to_name=%s""",
	# 	(doc.name))
	pdf_data=frappe.attach_print('Sales Order',doc.name, print_format='Sales Order Print')
	
	_file = frappe.get_doc({
	"doctype": "File",
	"file_name": pdf_data.get('fname'),
	"attached_to_doctype": "Sales Order",
	"attached_to_name": doc.name,
	"is_private": 1,
	"content": pdf_data.get('fcontent')
	})
	_file.save()



@frappe.whitelist()
def get_fg_item_for_consolidated_pick_list(doc):
	import json
	item_group = []
	doc = json.loads(doc)
	for row in doc.get("items"):
		item_group.append(row.get("item_group")) 
	fg_item_groups = frappe.db.sql("""SELECT item_group from `tabTable For Item Group`""",as_dict=1)
	fg_item_groups = [item.get('item_group') for item in fg_item_groups]

	item_group=list(set(item_group).intersection(fg_item_groups))
	return True if item_group else False


@frappe.whitelist()
def make_consolidated_pick_list(source_name, target_doc=None):
	from frappe.model.mapper import get_mapped_doc
	target_doc = get_mapped_doc("Sales Order", source_name, {
			"Sales Order": {
				"doctype": "Consolidated Pick List",
				"field_map": {
					"name": "sales_order",
				},
			}
		})
	return target_doc