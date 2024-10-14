{
	"name": "marel_in_data_report_purchase_o",
	"version": "17.0", 
	"depends": [
		"base",
		"sale",
		"purchase",
		"marel_in_data_stock_picking"
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
        # "data/product_data.xml",
		"view/marel_in_purchase.xml",
		# "view/in_marel_kode_dokumen.xml",
		# "view/menu.xml",
		# "report/inherit_coba_so.xml",
		#-----------------------------------------
		"report/marel_in_data_report_purchase_o.xml",
		#-------------------- coba PO
		"report/marel_report_po.xml",
		#-------------------------- report
		"report/report_marel_report_po_pemesanan_aksesoris_doc.xml",
		"report/report_marel_report_po_pemesanan_spare_parts_import_doc.xml",
		"report/report_marel_report_po_pemesanan_spare_parts_lokal_doc.xml",

		"report/report_marel_report_po_konfirmasi_pesanan_doc.xml",	
		"report/report_marel_report_po_konfirmasi_pesanan_doc_sale.xml",	
		"report/report_marel_report_po_konfirmasi_pesanan_2_in_1_doc.xml",
		# draff--------------------------------------------
		"report/report_marel_report_po_pemesanan_aksesoris_draff_doc.xml",
		"report/report_marel_report_po_pemesanan_spare_parts_import_draff_doc.xml",
		"report/report_marel_report_po_pemesanan_spare_parts_lokal_draff_doc.xml",
		# serat jalan--------------------------------- 
		"report/report_marel_report_surat_jalan_doc.xml",
		"report/report_marel_report_surat_jalan_doc_multi.xml",
		"report/report_marel_report_surat_jalan_doc_1.xml",
		#info orderan
		"report/report_marel_report_informasi_orderan_doc.xml",
		"report/report_marel_report_packing_list_doc.xml",
		"report/report_marel_report_po_informasi_order_doc.xml",
		"report/report_marel_report_kop_surat_doc.xml",

	],
	"installable": True,
	"auto_install": False,
    "application": True,
}