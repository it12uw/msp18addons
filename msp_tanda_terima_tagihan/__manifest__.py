{
	"name": "Tanda Terima Tagihan",
	"version": "18.0", 
	"depends": ["product","mrp"],
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
		"view/ir_sequence.xml",
		"view/menu_2.xml",
		"view/msp_tanda_terima_tagihan.xml",		
		"report/msp_tanda_terima_tagihan_menu.xml",
		"report/msp_tanda_terima_tagihan_template.xml",
		"security/ir.model.access.csv",
	],
	"installable": True,
	"auto_install": False,
    "application": True,
}