from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _
import base64
import csv
import io
import logging
from datetime import datetime

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Fields tambahan pada sale.order
    nomor_pesanan = fields.Char(string='No. Pesanan',index=True)
    order_status = fields.Selection([
        ('Belum Bayar', 'Belum Bayar'),
        ('Perlu Dikirim', 'Perlu Dikirim'),
        ('Sedang Dikirim', 'Sedang Dikirim'),
        ('Selesai', 'Selesai'),
        ('Batal', 'Batal'),
        ('Pengembalian', 'Pengembalian'),
        ('Pengiriman Gagal', 'Pengiriman Gagal')
    ], string='Status Pesanan')
    cancellation_return_status = fields.Char(string='Status Pembatalan/Pengembalian')
    tracking_number = fields.Char(string='No. Resi')
    opsi_pengiriman = fields.Char(string='Opsi Pengiriman')
    shipping_option = fields.Selection([
        ('antar counter', 'Antar Ke Counter'),
        ('pickup', 'Pick-up')
    ], string='Antar ke counter/pick-up')
    must_ship_before = fields.Datetime(string='Pesanan Harus Dikirimkan Sebelum')
    order_creation_time = fields.Datetime(string='Waktu Pesanan Dibuat')
    payment_time = fields.Datetime(string='Waktu Pembayaran Dilakukan')
    payment_method = fields.Char(string='Metode Pembayaran')
    seller_discount = fields.Float(string='Diskon Dari Penjual')
    platform_discount = fields.Float(string='Diskon Dari Shopee')
    voucher_seller = fields.Float(string='Voucher Ditanggung Penjual')
    cashback = fields.Float(string='Cashback Koin')
    voucher_platform = fields.Float(string='Voucher Ditanggung Shopee')
    package_discount = fields.Float(string='Paket Diskon')
    package_discount_platform = fields.Float(string='Paket Diskon (Diskon dari Shopee)')
    package_discount_seller = fields.Float(string='Paket Diskon (Diskon dari Penjual)')
    coin_discount = fields.Float(string='Potongan Koin Shopee')
    credit_card_discount = fields.Float(string='Diskon Kartu Kredit')
    shipping_fee_paid_by_buyer = fields.Float(string='Ongkos Kirim Dibayar oleh Pembeli') 
    shipping_fee_discount = fields.Float(string='Estimasi Potongan Biaya Pengiriman')
    return_shipping_fee = fields.Float(string='Ongkos Kirim Pengembalian Barang')
    estimated_shipping_fee = fields.Float(string='Perkiraan Ongkos Kirim')
    buyer_note = fields.Text(string='Catatan dari Pembeli')
    buyer_username = fields.Char(string='Username (Pembeli)')
    receiver_name = fields.Char(string='Nama Penerima')
    receiver_phone = fields.Char(string='No. Telepon')
    shipping_address = fields.Text(string='Alamat Pengiriman')
    city = fields.Char(string='Kota/Kabupaten')
    province = fields.Char(string='Provinsi')
    order_completion_time = fields.Datetime(string='Waktu Pesanan Selesai')
    amount_total = fields.Float(string='Estimasi Total Penghasilan', readonly=True, compute='_compute_amounts')
    sale_marketplace = fields.Many2one('market.place', string='Marketplace')
    

    # Untuk Odoo 17 fungsi _amount_all berubah menjadi _compute_amounts
    @api.depends('order_line.price_total')
    def _compute_amounts(self):
        for order in self:
            res = super(SaleOrder, self)._compute_amounts()
        return res

    @api.model
    def create(self, vals):
        if 'nomor_pesanan' in vals:
            vals['client_order_ref'] = vals['nomor_pesanan']
        return super(SaleOrder, self).create(vals)

    def write(self, vals):
        if 'nomor_pesanan' in vals:
            vals['client_order_ref'] = vals['nomor_pesanan']
        return super(SaleOrder, self).write(vals)        
    
    @api.constrains('order_status', 'order_completion_time')
    def _check_order_status(self):
        for order in self:
            if order.order_status == 'Selesai' and not order.order_completion_time:
                # Option 1: Set a default completion time
                order.order_completion_time = fields.Datetime.now()
                
                # Option 2: Raise a warning instead of an error
                # order._message_log(body=_("Warning: Pesanan ditandai sebagai 'Selesai' tanpa Waktu Pesanan Selesai."))
                
                # Option 3: Keep the validation, but make it less strict
                # if not self.env.context.get('importing_sale_order'):
                #     raise ValidationError(_("Waktu Pesanan Selesai harus diisi jika status pesanan adalah 'Selesai'."))


                # Inherit model stock.picking untuk menangani pembuatan dokumen pengiriman.
                # Dalam metode create, sistem akan memeriksa apakah picking terkait dengan sales order.
                # Jika ya, sistem mengisi carrier_tracking_ref (field untuk Tracking Reference) dengan nomor_pesanan dari sales order (sale_id.nomor_pesanan).
                # Kita juga mewarisi model sale.order untuk menangani konfirmasi pesanan.
                # Dalam metode action_confirm, setelah konfirmasi pesanan, sistem akan mengupdate semua picking yang belum selesai dengan nomor pesanan.

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            pickings = order.picking_ids.filtered(lambda x: x.state not in ('done', 'cancel'))
            for picking in pickings:
                picking.carrier_tracking_ref = order.nomor_pesanan
        return res            
    
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    parent_sku = fields.Char(string='Parent SKU')
    sku_reference = fields.Char(string='SKU Reference')
    variation_name = fields.Char(string='Variation Name')
    original_price = fields.Float(string='Harga Awal')
    discounted_price = fields.Float(string='Harga Setelah Diskon')
    returned_quantity = fields.Float(string='Returned Quantity', digits=(16, 6))
    product_weight = fields.Float(string='Product Weight', digits=(16, 6))
    total_weight = fields.Float(string='Total Weight', digits=(16, 6))
    biaya_administrasi = fields.Float(string='Biaya Administrasi', digits=(16,6))
    biaya_layanan = fields.Float(string='Biaya Layanan (Termasuk PPN 11%)', digits=(16,6))
    total = fields.Monetary(string='Sub Total', compute='_compute_amount', store=True)
    
    @api.depends('price_unit', 'discount', 'product_uom_qty', 'tax_id')
    def _compute_amount(self):
        for line in self:
            res = super(SaleOrderLine, self)._compute_amount()
    
    @api.onchange('original_price')
    def _onchange_original_price(self):
        if self.original_price:
            self.price_unit = self.original_price        

class SaleImportExport(models.Model):
    _name = 'sale.import.export'
    _description = 'Sale Import Export'

    def import_sale_data(self, csv_data):
        successful_imports = 0
        total_rows = 0
        error_rows = []

        # Decode CSV data if necessary
        if isinstance(csv_data, str):
            csv_file = io.StringIO(csv_data)
        elif isinstance(csv_data, bytes):
            csv_file = io.StringIO(csv_data.decode('utf-8'))
        else:
            csv_file = csv_data
        
        reader = csv.DictReader(csv_file)
        
        for row in reader:
            total_rows += 1
            try:
                self._process_sale_row(row)
                successful_imports += 1
            except Exception as e:
                error_rows.append((total_rows, str(e)))
                _logger.error(f"Error processing row {total_rows}: {str(e)}")
        
        return successful_imports, total_rows, error_rows


    def _process_sale_row(self, row):
        # Cari pesanan berdasarkan nomor pesanan
        order = self.env['sale.order'].search([('name', '=', row.get('No. Pesanan'))], limit=1)
        if not order:
            partner = self._get_or_create_partner(row)
            order_vals = {
                'name': row.get('No. Pesanan'),
                'partner_id': partner.id,
                'order_status': row.get('Status Pesanan'),
                'cancellation_return_status': row.get('Status Pembatalan/ Pengembalian'),
                'tracking_number': row.get('No. Resi'),
                'opsi_pengiriman': row.get('Opsi Pengiriman'),
                'shipping_option': 'antar counter' if row.get('Antar ke counter/pick-up') == 'Antar Ke Counter' else 'pickup',
                'must_ship_before': self._parse_datetime(row.get('Pesanan Harus Dikirimkan Sebelum')),
                'order_creation_time': self._parse_datetime(row.get('Waktu Pesanan Dibuat')),
                'payment_time': self._parse_datetime(row.get('Waktu Pembayaran Dilakukan')),
                'payment_method': row.get('Metode Pembayaran'),
                'seller_discount': self._parse_float(row.get('Diskon Dari Penjual', digits=(16, 6))),
                'platform_discount': self._parse_float(row.get('Diskon Dari Shopee', digits=(16, 6))),
                'voucher_seller': self._parse_float(row.get('Voucher Ditanggung Penjual', digits=(16, 6))),
                'cashback': self._parse_float(row.get('Cashback Koin', digits=(16, 6))),
                'voucher_platform': self._parse_float(row.get('Voucher Ditanggung Shopee', digits=(16, 6))),
                'package_discount': self._parse_float(row.get('Paket Diskon', digits=(16, 6))),
                'package_discount_platform': self._parse_float(row.get('Paket Diskon (Diskon dari Shopee)', digits=(16, 6))),
                'package_discount_seller': self._parse_float(row.get('Paket Diskon (Diskon dari Penjual)', digits=(16, 6))),
                'coin_discount': self._parse_float(row.get('Potongan Koin Shopee', digits=(16, 6))),
                'credit_card_discount': self._parse_float(row.get('Diskon Kartu Kredit', digits=(16, 6))),
                'shipping_fee_paid_by_buyer': self._parse_float(row.get('Ongkos Kirim Dibayar oleh Pembeli', digits=(16, 6))),
                'shipping_fee_discount': self._parse_float(row.get('Estimasi Potongan Biaya Pengiriman', digits=(16, 6))),
                'return_shipping_fee': self._parse_float(row.get('Ongkos Kirim Pengembalian Barang', digits=(16, 6))),
                'estimated_shipping_fee': self._parse_float(row.get('Perkiraan Ongkos Kirim', digits=(16, 6))),
                'buyer_note': row.get('Catatan dari Pembeli'),
                'buyer_username': row.get('Username (Pembeli)'),
                'receiver_name': row.get('Nama Penerima'),
                'receiver_phone': row.get('No. Telepon'),
                'shipping_address': row.get('Alamat Pengiriman'),
                'city': row.get('Kota/Kabupaten'),
                'province': row.get('Provinsi'),
                'order_completion_time': self._parse_datetime(row.get('Waktu Pesanan Selesai')),
            }
            order = self.env['sale.order'].create(order_vals)

        # Tambahkan data produk
        self._process_order_lines(order, row)
    
    def _process_order_lines(self, order, row):
        """
        Memproses detail produk per baris pesanan
        """
        product = self._get_or_create_product(row)
        line_vals = {
            'order_id': order.id,
            'product_id': product.id,
            'parent_sku': row.get('SKU Induk'),
            'sku_reference': row.get('Nomor Referensi SKU'),
            'variation_name': row.get('Nama Variasi'),
            'original_price': self._parse_float(row.get('Harga Awal')),
            'discounted_price': self._parse_float(row.get('Harga Setelah Diskon')),
            'returned_quantity': self._parse_float(row.get('Returned Quantity', 0.0)),
            'product_uom_qty': self._parse_float(row.get('Jumlah')),
            'product_weight': self._parse_float(row.get('Berat Produk')),
            'total_weight': self._parse_float(row.get('Total Berat')),
        }
        self.env['sale.order.line'].create(line_vals)

    def _get_or_create_partner(self, row):
        """
        Mendapatkan atau membuat mitra berdasarkan nama pembeli
        """
        partner = self.env['res.partner'].search([('name', '=', row.get('Username (Pembeli)'))], limit=1)
        if not partner:
            partner = self.env['res.partner'].create({
                'name': row.get('Username (Pembeli)'),
                'phone': row.get('No. Telepon'),
                'street': row.get('Alamat Pengiriman'),
                'city': row.get('Kota/Kabupaten'),
                'state_id': self._get_state_id(row.get('Provinsi')),
            })
        return partner
    
    def _get_state_id(self, state_name):
        """
        Mendapatkan ID provinsi berdasarkan nama
        """
        state = self.env['res.country.state'].search([('name', '=', state_name)], limit=1)
        if state:
            return state.id
        return False

    def _get_or_create_product(self, row):
        """
        Mendapatkan atau membuat produk berdasarkan SKU
        """
        product = self.env['product.product'].search([('default_code', '=', row.get('Nomor Referensi SKU'))], limit=1)
        if not product:
            product = self.env['product.product'].create({
                'name': row.get('Nama Produk'),
                'default_code': row.get('Nomor Referensi SKU'),
                'list_price': self._parse_float(row.get('Harga Awal')),
                'weight': self._parse_float(row.get('Berat Produk')),
            })
        return product
    
    def _parse_float(self, value):
        """
        Parse value to float, handling empty cases and preserving precision
        """
        if not value:
            return 0.0
        try:
            # Remove thousand separators and replace comma with dot for decimal
            cleaned_value = value.replace(',', '').replace('.', '').replace(',', '.')
            return float(cleaned_value)
        except ValueError:
            return 0.0

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def create(self, vals):
        res = super(StockPicking, self).create(vals)
        if res.sale_id and res.sale_id.nomor_pesanan:
            res.carrier_tracking_ref = res.sale_id.nomor_pesanan
        return res



    