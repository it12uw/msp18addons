from odoo.addons import decimal_precision as dp
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from odoo.tools import float_round

class SampleGramasiProductList(models.Model):

    _name = 'sample.gramasi.product.list'
    #_rec_name = 'product_template_id'

    sample_gramasi_id = fields.Many2one('sample.gramasi',string=u'sample_gramasi_id',)
    #------------
    product_template_id = fields.Many2one('product.product',string=u'Nama Benang',)
    qty = fields.Float(string=u'Qty Benang Per Pasang (kg)',digits=dp.get_precision('Product Unit of Measure'),required=True,)
    qty_bom = fields.Float(string=u'Qty Bom',digits=dp.get_precision('Product Unit of Measure'))
    partner_id = fields.Many2one('res.partner', string='Customer', )

    def get_hitung_qty_bom_line(self):
        self.qty_bom = 0.0
        toleransi_qty_bom = (self.qty*0.07)
        self.qty_bom = (self.qty + toleransi_qty_bom)
        return

class SampleGramasi(models.Model):

    _name = 'sample.gramasi'
    _rec_name = 'nama_kaoskaki'

    sample_gramasi_product_list_line = fields.One2many('sample.gramasi.product.list','sample_gramasi_id',string=u'Sample Gramasi List',)
    #-------------------------------------
    tgl = fields.Date(string=u'Tgl',default=fields.Date.context_today,)
    nama_kaoskaki = fields.Char(string=u'Nama Sample Kaos Kaki',required=True,)
    waktu = fields.Integer(string=u'Waktu (menit)',)
    berat_kaos_kaki = fields.Float(string=u'Berat KaosKaki (Kg)',digits=dp.get_precision('Product Unit of Measure'),)
    status = fields.Boolean(string=u'Fix',)
    size = fields.Char(string=u'Size',)
    style = fields.Char(string=u'Style',)
    artikel = fields.Char(string=u'Artikel',)
    partner_id = fields.Many2one('res.partner', string='Customer',)
