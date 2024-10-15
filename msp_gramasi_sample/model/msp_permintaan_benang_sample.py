from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class MarelinPermintaanBenangSampleList(models.Model):
    _name = 'marelin.permintaan.benang.samplelist'
    # _rec_name = 'permintaan_benang_sample_id'
    
    # relasi untuk one2many
    
    permintaan_benang_sample_id = fields.Many2one('marelin.permintaan.benang.sample',string=u'Nama Desain Id',)
    # fields untuk ambil data nama desain
    product_template_id = fields.Many2one('product.product',string=u'Nama Benang',)
    jmlh_ambil_kg = fields.Float(string=u'Jumlah Ambil Kg',)
    jmlh_ambil_connes = fields.Float(string=u'Jumlah Ambil Connes',)
    jmlh_sisa_kg = fields.Float(string=u'Jumlah Sisa Kg',)
    jmlh_sisa_connes = fields.Float(string=u'Jumlah Sisa Connes',)
    keterangan = fields.Text(string=u'Keterangan',)
    partner_id = fields.Many2one('res.partner', string='Customer', )
    

class MarelInPermintaanBenangSample(models.Model):

    _name = 'marelin.permintaan.benang.sample'
    _rec_name = 'nama_desain_sample'    
    # penghubung fields many2one permintaan.benang.sample.list
    permintaan_benang_sample_list_line = fields.One2many('marelin.permintaan.benang.samplelist','permintaan_benang_sample_id',string=u'Sample Gramasi List',)
    tgl = fields.Date(string=u'Tanggal',default=fields.Date.context_today,readonly=True,)
    needle = fields.Char(string=u'Needle',)
    nama_desain_sample = fields.Char(string=u'Nama Desain',required=True,)
    partner_id = fields.Many2one('res.partner', string='Customer',)