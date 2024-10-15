{
	"name": "Gramasi Sample MSP",
	"version": "18.0", 
	"depends": [
		"base","product",
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
        'security/ir.model.access.csv',
		"view/msp_gramasi_sample_menu.xml",
		"view/msp_gramasi_sample.xml",		
		"view/msp_permintaan_benang_sample.xml",
		# report------		
		# "report/marel_report_sample.xml",		
		# "report/report_marel_report_sample_perminataan_benang_doc.xml",		
	],
	"installable": True,
	"auto_install": False,
    "application": True,
}