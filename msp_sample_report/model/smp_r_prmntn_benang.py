from odoo import models, fields, api, _
import logging
# _logger = logging.getLogger(__name__)


class SampleReportPermintaanBenang(models.AbstractModel):
    """
    Class untuk Custom Data Report sebelum di render ke dalam template
    """
    _name = 'report.msp_sample_report.smp_r_prmntn_benang'

    @api.model
    def get_report_values(self, docids, data=None):
        """
        Method default custom reporting odoo untuk custom data

        params:
            - docids = id record model yg akan digenerate didalam report
            - data = biasanya digunakan untuk custom report dengan data dari Wizard
        """
        # report_obj = self.env['report']
        # report = report_obj._get_report_from_name('manufacturing_bom_report.report_mrpbomorder')
        
        msd2 = self.env['msp.sample.dev'].browse(docids)

        # Ambil data mo yg akan ditampilan di report, dimasukan ke dict dengan key id 
        # agar product dengan nama tidak tertumpuk
        # karena dikelompokkan oleh id
        data = {}
        for order in msd2:
            for record in order.mrp_bom_line_ids:
                if record.product_id.product_tmpl_id.categ_id.id==36 or record.product_id.product_tmpl_id.categ_id.id==37 :
                    if record.product_id.id in data:
                        data[record.product_id.id]['qty'] += record.jumlah_ambil
                    else:
                        data[record.product_id.id] = {'name':record.product_id.name,'qty':record.jumlah_ambil,}
                        # data[record.product_id.id] = {'name': record.product_id.name, 'qty': record.jumlah_ambil}
        # masukkan ke dalam list tanpa key untuk mempermudah sorting
        # bisa di improve dengan library Pandas (untuk olah data) dan Jinja (templating report) agar lebih efektif
        data_without_key = []
        for key in data:
            data_without_key.append(data[key])


        #, 'delivery_date': record.production_id.
        docargs = {
            'msd2' : ", ".join(order.name for order in msd2),
            'nama_sample' : ", ".join(order.nama_sample for order in msd2),
            'needle' : ", ".join(order.needle for order in msd2),
            'tgl_bon' : ", ".join(order.tgl_bon for order in msd2),
            # 'halaman_bom' : ", ".join(order.kode_dokumen_bagian_id.halaman_bom for order in mo),
            # 'no_revisi_bom' : ", ".join(order.kode_dokumen_bagian_id.no_revisi_bom for order in mo),
            # 'tgl_revisi_bom' : ", ".join(order.kode_dokumen_bagian_id.tgl_revisi_bom for order in mo),
            # 'tgl_efektif_bom' : ", ".join(order.kode_dokumen_bagian_id.tgl_efektif_bom for order in mo),
            'data': sorted(data_without_key, key=lambda key: key['name']) # sorting by name
        }

        # return self.env["report"].render('manufacturing_bom_report_new.report_mrpbomorder_new', docargs)
        return docargs
            