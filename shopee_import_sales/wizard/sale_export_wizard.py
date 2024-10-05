from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64
import csv
import io
from datetime import datetime

class SaleExportWizard(models.TransientModel):
    _name = 'sale.export.wizard'
    _description = 'Sale Export Wizard'

    date_from = fields.Date(string='Date From', required=True)
    date_to = fields.Date(string='Date To', required=True)
    partner_ids = fields.Many2many('res.partner', string='Customers')
    export_file = fields.Binary(string='Export File', readonly=True)
    filename = fields.Char(string='Filename', default='sale_export.csv')

    @api.onchange('date_from')
    def _onchange_date_from(self):
        if self.date_from and self.date_to and self.date_from > self.date_to:
            self.date_to = self.date_from

    def action_export(self):
        self.ensure_one()
        
        # Define the domain for sale orders
        domain = [
            ('date_order', '>=', self.date_from),
            ('date_order', '<=', self.date_to),
        ]
        if self.partner_ids:
            domain.append(('partner_id', 'in', self.partner_ids.ids))

        # Fetch sale orders
        sale_orders = self.env['sale.order'].search(domain)

        if not sale_orders:
            raise UserError(_("No sale orders found for the selected criteria."))

        # Prepare CSV data
        output = io.StringIO()
        writer = csv.writer(output)

        # Write header
        header = [
            'No. Pesanan', 'Status Pesanan', 'Status Pembatalan/ Pengembalian', 'No. Resi',
            'Opsi Pengiriman', 'Antar ke counter/pick-up', 'Pesanan Harus Dikirimkan Sebelum',
            'Waktu Pesanan Dibuat', 'Waktu Pembayaran Dilakukan', 'Metode Pembayaran',
            'Diskon Dari Penjual', 'Diskon Dari Shopee', 'Voucher Ditanggung Penjual',
            'Cashback Koin', 'Voucher Ditanggung Shopee', 'Paket Diskon',
            'Paket Diskon (Diskon dari Shopee)', 'Paket Diskon (Diskon dari Penjual)',
            'Potongan Koin Shopee', 'Diskon Kartu Kredit', 'Ongkos Kirim Dibayar oleh Pembeli',
            'Estimasi Potongan Biaya Pengiriman', 'Ongkos Kirim Pengembalian Barang',
            'Perkiraan Ongkos Kirim', 'Catatan dari Pembeli', 'Username (Pembeli)',
            'Nama Penerima', 'No. Telepon', 'Alamat Pengiriman', 'Kota/Kabupaten', 'Provinsi',
            'Waktu Pesanan Selesai', 'SKU Induk', 'Nomor Referensi SKU', 'Nama Produk',
            'Nama Variasi', 'Harga Awal', 'Harga Setelah Diskon', 'Jumlah', 'Berat Produk',
            'Total Berat'
        ]
        writer.writerow(header)

        # Write data
        for order in sale_orders:
            for line in order.order_line:
                row = [
                    order.nomor_pesanan, order.order_status, order.cancellation_return_status,
                    order.tracking_number, order.opsi_pengiriman, order.shipping_option,
                    order.must_ship_before, order.order_creation_time, order.payment_time,
                    order.payment_method, order.seller_discount, order.platform_discount,
                    order.voucher_seller, order.cashback, order.voucher_platform,
                    order.package_discount, order.package_discount_platform,
                    order.package_discount_seller, order.coin_discount, order.credit_card_discount,
                    order.shipping_fee_paid_by_buyer, order.shipping_fee_discount,
                    order.return_shipping_fee, order.estimated_shipping_fee, order.buyer_note,
                    order.buyer_username, order.receiver_name, order.receiver_phone,
                    order.shipping_address, order.city, order.province, order.order_completion_time,
                    line.parent_sku, line.sku_reference, line.product_id.name, line.variation_name,
                    line.original_price, line.discounted_price, line.product_uom_qty,
                    line.product_weight, line.total_weight
                ]
                writer.writerow(row)

        # Encode the CSV data
        export_data = output.getvalue().encode()
        
        # Set the binary field and filename
        self.export_file = base64.b64encode(export_data)
        self.filename = f'sale_export_{self.date_from}_{self.date_to}.csv'

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.export.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }