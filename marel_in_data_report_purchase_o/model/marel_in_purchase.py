from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_round

class MarelInPurchase(models.Model):
    _inherit = ['purchase.order']
    
    no_pajak = fields.Char(string='No/Faktur Pajak',)
    surat_jalan = fields.Char(string='Surat Jalan',)
    kurs = fields.Float(string=u'Jumlah Kurs',)
    jenis_kurs = fields.Selection(string=u'Jenis Kurs',selection=[('kurs_tengah_bi', 'Kurs Tengah BI'), ('kurs_pajak', 'Kurs Pajak'), ('kurs_averydennison', 'Kurs Averydennison')])
    scheduled_date = fields.Date(string='Scheduled Date',default=fields.Date.context_today,store=True)
    taxes_id = fields.Char(string='Taxes',related='order_line.taxes_id.name', )

class MarelInPurchaseLine(models.Model):
    _inherit = ['purchase.order.line']

    status = fields.Selection(string=u'Status', selection=[('Celup', 'Celup'), ('Beli', 'Beli'), ('Maklon', 'Maklon')], store=True)
    kurs = fields.Float(string=u'Kurs', store=True)
    keterangan = fields.Text(string=u'Keterangan', store=True)
    harga_dolar = fields.Float(string=u'Hrga USD', digits=dp.get_precision('Custom 1'), default=1.0, store=True)
    ket_gramasi = fields.Boolean(string=u'Kurs ?', store=True)

    # Menggunakan compute field untuk mengambil nilai standard_price dari tipe json atau float
    standard_price_product = fields.Float(string=u'Hrga USD', compute='_compute_standard_price_product', readonly=True, store=True)

    @api.depends('product_id.standard_price')
    def _compute_standard_price_product(self):
        for line in self:
            if line.product_id and line.product_id.standard_price:
                if isinstance(line.product_id.standard_price, dict):
                    # Jika standard_price adalah json, ambil nilai yang sesuai
                    line.standard_price_product = line.product_id.standard_price.get('price', 0.0)
                else:
                    # Jika standard_price adalah float, gunakan nilainya langsung
                    line.standard_price_product = line.product_id.standard_price
            else:
                line.standard_price_product = 0.0

    @api.onchange('ket_gramasi')
    def get_purchase_menggunakan_kurs(self):
        if self.ket_gramasi:
            self.price_unit = (self.order_id.kurs * self.harga_dolar)
        return
