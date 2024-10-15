from odoo.addons import decimal_precision as dp
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from odoo.tools import float_round

class MspTandaterimaTagihanLine(models.Model):
    _name = 'msp.tandaterima.tagihan.line'
    _rec_name = 'keterangan'

    msp_tanda_terima_tagihan_id = fields.Many2one('msp.tanda.terima.tagihan',string=u'Keterangan',)
    keterangan = fields.Char(string='Keterangan',)
    nominal = fields.Float(string='Nominal',digits=dp.get_precision('Custom 3'),)

class MspTandaTerimaTagihan(models.Model):
    _name = 'msp.tanda.terima.tagihan'
    
    msp_tanda_terima_tagihan_line_ids = fields.One2many('msp.tandaterima.tagihan.line','msp_tanda_terima_tagihan_id',string=u'Keterangan',)

    def get_msp_tanda_terima_tagihan_no(self):
        nama_baru = self.env['ir.sequence'].next_by_code('msp.tanda.terima.tagihan.no')
        return nama_baru
      
    name = fields.Char(string='Id Sample',required=True,copy=False, default=get_msp_tanda_terima_tagihan_no,readonly=True )
    partner_id = fields.Many2one('res.partner', string='Customer',)
    nama_pengirim = fields.Char(string='Nama Pengirim',)
    tanggal = fields.Date(string='Tanggal',default=fields.Date.context_today,)
    keterangan = fields.Char(string='Keterangan',)
    nama_ttd = fields.Char(string='Nama',)
    #-------------------------------------
    total_nominal = fields.Float(string='Total',compute='_get_nominal',store=True)
    nominal = fields.Float(string='Nominal',digits=dp.get_precision('Custom 3'),)

    # @api.multi
    @api.depends('msp_tanda_terima_tagihan_line_ids')
    def _get_nominal(self):
        for msp_tanda_terima_tagihan_id in self:
            msp_tanda_terima_tagihan_id.total_nominal = sum((line_id.nominal) for line_id in msp_tanda_terima_tagihan_id.msp_tanda_terima_tagihan_line_ids)
