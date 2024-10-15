from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
import odoo.addons.decimal_precision as dp

class MesinMarelProduksi(models.Model):
	_name = 'mesin.marel.produksi'
	_description = u'mesin marel produksi'

	_rec_name = 'nama_mesin_blok'

	nama_mesin_blok = fields.Char(string=u'Nama Mesin',required=True,)
	no_serial_number = fields.Char(string=u'Serial Number',required=True,)
	tahun = fields.Integer(string='Tahun Mesin', required=True)
	jml_jarum = fields.Integer(string=u'Jumlah Jarum',required=True,)
	type_mesin = fields.Many2one('type.mesin.produksi', string='Type Mesin/No Mesin',)
	merk = fields.Many2one('merk.mesin.produksi', string='Merk Mesin',)
	needls = fields.Char(string=u'Needls',)
	gauge = fields.Char(string=u'Gauge',)
	diameter = fields.Char(string=u'Diameter',)

class MerkMesinProduksi(models.Model):
	_name ='merk.mesin.produksi'
	_description = "Merk Mesin Produksi Marel"

	merk_mesin = fields.Char(string="Merk", required=True)

	def name_get(self):
		result = [] 
		for record in self:
			name = record.merk_mesin 
			result.append((record.id, name))
		return result 

class TypeMesinProduksi(models.Model):
	_name ='type.mesin.produksi'
	_description = "Type Mesin Produksi Marel"

	type_mesin = fields.Char(string="Type Mesin/No Mesin", required=True)
	
	def name_get(self):
			result = [] 
			for record in self:
				name = record.type_mesin 
				result.append((record.id, name))
			return result 

class NamaTeknisi(models.Model):
	_name = 'nama.teknisi'   
	_rec_name = 'nama_teknisi'
	
	nama_teknisi = fields.Char(string=u'Nama Teknisi',)

class NamaTeknisiMesinList(models.Model):
	_name = 'nama.teknisi.mesin.list'   
	_rec_name = 'nama_teknisi_ids'

	nama_teknisi_ids = fields.Many2one('nama.teknisi',string=u'Teknisi',)
	jenis_kerusakan_mesinmarel_list_id = fields.Many2one('jenis.kerusakan.mesinmarellist', 'Jenis Kerusakan Mesin List')
	# jam perbaikan	
	jam_mulai_perbaikan = fields.Datetime(string=u'Mulai Perbaikan', readonly='True')
	jam_perbaikan_selesai = fields.Datetime(string=u'Selesai Perbaikan',readonly='True')
	selesai = fields.Boolean(string=u'Selesai', readonly='True',)
	blm_selesai = fields.Boolean(string=u'Belum Selesai', readonly='True',)
	timer_duration = fields.Float(invisible=1, string='Time Duration (Minutes)',readonly='True')
	shift = fields.Selection([
        ('A',_('A')),
        ('B',_('B')),
	    ('C',_('C')),
		('MTC',_('MTC'))], string="Shift",)

	def action_jam_mulai(self):
		jam_mulai_perbaikan = fields.Datetime.now()
		self.write({'jam_mulai_perbaikan':jam_mulai_perbaikan})
	def action_jam_selesai(self):
		jam_perbaikan_selesai = fields.Datetime.now()
		self.write({'jam_perbaikan_selesai': jam_perbaikan_selesai, 'selesai': True})
		if self.jam_mulai_perbaikan:
			durasi = fields.Datetime.from_string(jam_perbaikan_selesai) - fields.Datetime.from_string(self.jam_mulai_perbaikan)
			self.timer_duration = round(durasi.total_seconds() / 60.0, 2)
		else:
			return False
			return True

	def action_belum_selesai(self):
		self.write({'blm_selesai' : True,})
		durac = fields.Datetime.from_string(self.jam_perbaikan_selesai) - fields.Datetime.from_string(self.jam_mulai_perbaikan)
		self.timer_duration = round(durac.total_seconds() / 60.0, 2)
		return True


class JenisKerusakanMesinMarel(models.Model):
	_name = 'jenis.kerusakan.mesinmarel'
	_description = u'jenis kerusakan mesin marel'
	_rec_name = 'jenis_kerusakan'
	
	jenis_kerusakan = fields.Char(string=u'Jenis Kerusakan',required=True,)

	
class JenisKerusakanMesinMarelList(models.Model):

	_name = 'jenis.kerusakan.mesinmarellist'
	_description = u'jenis kerusakan mesi marel list'
	_rec_name = 'jenis_kerusakan_mesinmarel_id'

	#relasi one2many 
	kerusakan_list_mesin_id = fields.Many2one('kerusakan.list.mesin', 'List Kerusakan Mesin')
	#FIELDS BIASA
	jenis_kerusakan_mesinmarel_id = fields.Many2one('jenis.kerusakan.mesinmarel', 'Jenis Kerusakan')
	nama_teknisi_line = fields.One2many('nama.teknisi.mesin.list','jenis_kerusakan_mesinmarel_list_id',string=u'Nama Teknisi',required=True,)
	selesai = fields.Boolean(string=u'Selesai', readonly='True',)
	blm_selesai = fields.Boolean(string=u'Blm Selesai', readonly='True',)

	def action_belum_selesai(self):
		self.write({'blm_selesai' : True,})
		return True
	def action_selesai(self):
		self.write({'selesai' : True,})
		return True


class KerusakanListMesin(models.Model):

	_name = 'kerusakan.list.mesin'
	_description = u'kerusakan list mesin'

	mesin_produksi_id = fields.Many2one('mesin.marel.produksi',string=u'Nama/Blok Mesin',required=True,)	
	jenis_kerusakan_mesinmarel_line = fields.One2many('jenis.kerusakan.mesinmarellist','kerusakan_list_mesin_id',string=u'Kerusakan Mesin',required=True,)
	jam_create = fields.Datetime(string=u'Jam Create',default=fields.Datetime.now, readonly='True')
	#versi jam fields
	jam_mulai_perbaikan = fields.Datetime(string=u'Mulai Perbaikan', readonly='True')
	jam_perbaikan_selesai = fields.Datetime(string=u'Selesai Perbaikan',readonly='True')
	note = fields.Text(string=u'Note',)
	selesai_perbaikan = fields.Boolean(string=u'Telah di Perbaiki',readonly='true',)
	#-------------
	#versi float
	# waktu_mulai = fields.Float(string=u'Waktu Mulai',)
	# waktu_selesai = fields.Float(string=u'Waktu Selesai',)
	#--------------------
	# selisih_waktu = fields.Char(string=u'Selisih Waktu',)	
	state = fields.Selection([('draft', 'Open'),
							('open','Run'),('done','Done'),('cancel','Canceled')],
							string="Status", readonly=True, copy=False, default='draft')
	def action_confrim(self):
		jam_mulai_perbaikan = fields.Datetime.now()
		self.write({'state':'open','jam_mulai_perbaikan':jam_mulai_perbaikan})
	def action_done(self):
		jam_perbaikan_selesai = fields.Datetime.now()
		self.write({'state': 'done','selesai_perbaikan': True,'jam_perbaikan_selesai':jam_perbaikan_selesai,})

	def action_cancel(self):
		self.write({'state': 'cancel','is_locked' : True,})
		return True

	# @api.onchange('waktu_selisih_waktu')
	# def get_waktu_selisih_waktu(self):
	# 	self.selisih_waktu = self.waktu_selesai - self.waktu_mulai
	# 	self.selesai_perbaikan = True
		