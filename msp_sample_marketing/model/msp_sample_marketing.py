from odoo.addons import decimal_precision as dp
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime
import logging
# from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from odoo.tools import float_round

class MarelinSampleMarketing(models.Model):
    _name = 'msp.sample.marketing'
    
    def get_msp_sample_marketing_no(self):
        nama_baru = self.env['ir.sequence'].next_by_code('marelin.sample.marketing.no')
        return nama_baru
    
    name = fields.Char(string='Id Sample',required=True,copy=False, default=get_msp_sample_marketing_no,readonly=1 )
    partner_id = fields.Many2one('res.partner', string='Customer',)
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, default=lambda self: self.env.user)
    sale_id2 = fields.Many2one('sale.order',string='No SO')
    # sale_id = fields.Many2one('sale.order', 'Ref SO')
    gramasi_option = fields.Selection([
        ('Ya', 'Ya'),
        ('Tidak','Tidak'),
        ],string="Gramasi",copy=False)

    form = fields.Selection([
        ('Baru', 'Baru'),
        ('Revisi','Revisi'),
        ('Buat_Ulang','Buat_Ulang'),
        ],string="Form",copy=False)
    gambar_sample_marketing = fields.Binary(string='Gambar Sample',)
    jumlah_sample = fields.Integer(string='Jumlah Sample',)

    tanggal = fields.Date(string='Tanggal',default=fields.Date.context_today,)
    brand = fields.Char(string='Brand',)
    
    model_sample = fields.Selection(string=u'Model',selection=[
        ('Soccer', 'Soccer'),
        ('Crew', 'Crew'),
        ('Quarter', 'Quarter'),
        ('Ankle', 'Ankle'),
        ('Liner', 'Liner'),
        ('Super_Low', 'Super Low'),
        ('Other', 'Other'),])

    standar = fields.Selection(string=u'Standar/Acuan',selection=[
        ('Original_Sample', 'Original Sample'),
        ('Work_Sheet', 'Tech Pack/Design'),
        ('Approval_From_Marel', 'Approval From Marel'),])
        
    komposisi_material = fields.Text(string='Komposisi Material',)
    jarum = fields.Char(string='Jarum',)
    target_gramasi_bruto_sample = fields.Char(string='Target Gramasi Bruto Sample',)
    netto_original_sample = fields.Char(string='Netto Original Sample',)

    gum_stretch_x= fields.Char(string='Gum Stretch x ',)
    gum_stretch_y= fields.Char(string='Gum Stretch y ',)
    gum_relaxed_x= fields.Char(string='Gum Relaxed x ',)
    gum_relaxed_y= fields.Char(string='Gum Relaxed y ',)

    leg_gum_stretch_x= fields.Char(string='Leg Gum Stretch x ',)
    leg_gum_stretch_y= fields.Char(string='Leg Gum Stretch y ',)
    leg_gum_relaxed_x= fields.Char(string='Leg Gum Relaxed x ',)
    leg_gum_relaxed_y= fields.Char(string='Leg Gum Relaxed y ',)

    leg_gum_atas_stretch_x= fields.Char(string='Leg Gum Atas Stretch x ',)
    leg_gum_atas_stretch_y= fields.Char(string='Leg Gum Atas Stretch y ',)
    leg_gum_atas_relaxed_x= fields.Char(string='Leg Gum Atas Relaxed x ',)
    leg_gum_atas_relaxed_y= fields.Char(string='Leg Gum Atas Relaxed y ',)

    leg_gum_bawah_stretch_x= fields.Char(string='Leg Gum Bawah Stretch x ',)
    leg_gum_bawah_stretch_y= fields.Char(string='Leg Gum Bawah Stretch y ',)
    leg_gum_bawah_relaxed_x= fields.Char(string='Leg Gum Bawah Relaxed x ',)
    leg_gum_bawah_relaxed_y= fields.Char(string='Leg Gum Bawah Relaxed y ',)

    leg_stretch_x= fields.Char(string=' Leg Stretch x',)
    leg_stretch_y= fields.Char(string='Leg Stretch y ',)
    leg_relaxed_x= fields.Char(string=' Leg Relaxed x',)
    leg_relaxed_y= fields.Char(string='Leg Relaxed y ',)

    foot_stretch_x= fields.Char(string=' Foot Stretch x',)
    foot_stretch_y= fields.Char(string=' Foot Stretch y',)
    foot_relaxed_x= fields.Char(string=' Foot Relaxed x',)
    foot_relaxed_y= fields.Char(string=' Foot Relaxed y',)

    foot_gum_stretch_x= fields.Char(string='Foot Gum Stretch x ',)
    foot_gum_stretch_y= fields.Char(string='Foot Gum Stretch y ',)
    foot_gum_relaxed_x= fields.Char(string='Foot Gum Relaxed x ',)
    foot_gum_relaxed_y= fields.Char(string='Foot Gum Relaxed y ',)

    hell_stretch_x= fields.Char(string='Heel Stretch x ',)
    hell_stretch_y= fields.Char(string='Heel Stretch y ',)
    hell_relaxed_x= fields.Char(string='Heel Relaxed x ',)
    hell_relaxed_y= fields.Char(string='Heel Relaxed y ',)

    mesin = fields.Selection([
        ('132', '132'),
        ('156','156'),
        ('160','160'),
        ('132_Star','132 Star'),
        ('168','168'),
        ('200','200'),
        ('Lonati','Lonati'),
        ('Fantasi','Fantasi'),
        ('Star','Star'),
        ('Hitech','Hitech'),
        ('Mesin_Headband','Mesin Headband'),
        ],string="Mesin",copy=False)

    
    jenis = fields.Selection([
        ('Plainmesh', 'Plainmesh'),
        ('HalfTerry','HalfTerry'),
        ('FullTerry','FullTerry'),
        ('HighTerry','HighTerry'),
        ('FullElastic','FullElastic'),
        ],string="jenis",copy=False)

    rib_khusus_knit = fields.Selection([
        ('1x1', '1x1'),
        ('3x1','3x1'),
        ('2x1','2x1'),
        ('Tidak Ada','Tidak Ada'),
        ],string="RIB Khusus RIB Knit",copy=False)

    rib_cuff = fields.Selection([
        ('1x1', '1x1'),
        ('3x1','3x1'),
        ('2x1','2x1'),
        ('Tidak Ada','Tidak Ada'),
        ],string="RIB Cuff",copy=False)

    rib_leg_gum_atas = fields.Selection([
        ('1x1', '1x1'),
        ('3x1','3x1'),
        ('2x1','2x1'),
        ('Tidak Ada','Tidak Ada'),
        ],string="RIB Leg Gum Atas",copy=False)

    rib_leg_gum_bawah = fields.Selection([
        ('1x1', '1x1'),
        ('3x1','3x1'),
        ('2x1','2x1'),
        ('Tidak Ada','Tidak Ada'),
        ],string="RIB Leg Gum Bawah",copy=False)

    rib_foot_gum = fields.Selection([
        ('1x1', '1x1'),
        ('3x1','3x1'),
        ('2x1','2x1'),
        ('Tidak Ada','Tidak Ada'),
        ],string="RIB Foot Gum",copy=False)

    embroidery = fields.Selection([
        ('Ya', 'Ya'),
        ('Tidak','Tidak'),
        ],string="Embroidery",copy=False)
    ukuran_embroidery = fields.Char(string='Ukuran Embroidery',)
    posisi_embroidery = fields.Char(string='Posisi Embroidery',)
    
    anti_slip = fields.Selection([
        ('Ya', 'Ya'),
        ('Tidak','Tidak'),
        ],string="Anti Slip",copy=False)
    ukuran_anti_slip = fields.Char(string='Ukuran Anti Slip',)
    posisi_anti_slip = fields.Char(string='Posisi Anti Slip',)

    jahit_no_show = fields.Selection([
        ('Ya', 'Ya'),
        ('Tidak','Tidak'),
        ('Model_Langsung','Model Langsung'),
        ],string="Jahit No Show",copy=False)
    
    satuan = fields.Selection([
        ('Pcs', 'Pcs'),
        ('Pair','Pair'),
        ],string="Satuan",copy=False)
    
    posisi_logo = fields.Char(string='Posisi Logo',)
    ukuran_logo = fields.Char(string='Ukuran Logo',)
    
    target_finish_sample = fields.Text(string='Target Finish Sample',)
    lokasi_folder_file_soft_copy = fields.Text(string='Lokasi Folder File Soft Copy',)
    material_packing = fields.Text(string='Material Packing',)
    informasi_lainnya = fields.Text(string='Informasi Lainnya',)
