from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class InMarelKodeDokumen(models.Model):
    _name = 'inmarel.kode.dokumen'
    _rec_name = 'devisi'

    devisi = fields.Char(string=u'Devisi',)
    kode_dokumen = fields.Char(string=u'Kode Dokumen',)
    # hal = fields.Integer(string=u'Hal',)
    halaman = fields.Char(string=u'Halaman',)
    no_revisi = fields.Integer(string=u'No Revisi',)
    tgl_revisi = fields.Date(string=u'Tgl Revisi',)
    tgl_efektif = fields.Date(string=u'Tgl Efektif',)
    
class InMarelPurchaseOrder(models.Model):
    _inherit = ['purchase.order']
    _rec_name = 'nama_devisi'
    
    nama_devisi = fields.Many2one('inmarel.kode.dokumen',string=u'Kode Dokumen Devisi',)

class InMarelSaleOrder(models.Model):
    _inherit = ['sale.order']
    _rec_name = 'nama_devisi'
    
    nama_devisi = fields.Many2one('inmarel.kode.dokumen',string=u'Kode Dokumen Devisi',)
    no_po_customer = fields.Char(string=u'No PO Customer',)
    