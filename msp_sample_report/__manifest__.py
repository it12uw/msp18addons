{
	"name": "msp_sample_report",
	"version": "18.0", 
	"depends": [
		"base",
		"product",
		"msp_sample",
	],
	"author": "asrent345@gmail.com", 
	"category": "Education", 
	'website': 'http://www.vitraining.com',
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
		"view/bom_report_act.xml",
		"view/sample_report_permintaan_benang_template.xml",
		"view/sample_report_permintaan_aksesoris_template.xml",

		"report/marel_in_samlpe_dev_2_menu.xml",
		"report/marel_in_samlpe_dev_2_template.xml",
		"report/report_marel_in_permintaan_benang_develop_doc.xml",
	],
	"installable": True,
	"auto_install": False,
    "application": True,
}