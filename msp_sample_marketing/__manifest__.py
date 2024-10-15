{
	"name": "Sample Marketing Marel Sukses Pratama",
	"version": "18.0", 
	"depends": [
		"base",
		"product",
		"sale",
	],
	"author": "asrent345@gmail.com", 
	"category": "Marketing", 
	'website': '',
	'depends': ['base', 'web', 'sale'],
	"description": """\
Manage
======================================================================

* this is my academic information system module
* created menu:
* created object
* created views
* logic:

""",
	"data": [
        "security/ir.model.access.csv",
		"view/msp_sample_marketing_menu.xml",
		"view/msp_sample_marketing_view.xml",			
		"report/msp_form_pengajuan_sample.xml",
		"report/msp_menu_sample_marketing.xml",
	],
	"installable": True,
	"auto_install": False,
    "application": True,
}