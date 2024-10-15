from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import base64
import csv
import io
import logging
from datetime import datetime

_logger = logging.getLogger(__name__)

try:
    import pytz
except ImportError:
    pytz = None
    _logger.warning("pytz library is not installed. Timezone conversion may not be accurate.")

class SaleImportWizard(models.TransientModel):
    _name = 'sale.import.wizard'
    _description = 'Sale Import Wizard'

    file_data = fields.Binary(string='File CSV', required=True)
    filename = fields.Char(string='Filename')

    def _parse_file(self):
        data = base64.b64decode(self.file_data)
        encodings = ['utf-8', 'iso-8859-1', 'windows-1252']
        for encoding in encodings:
            try:
                file_input = io.StringIO(data.decode(encoding))
                reader = csv.DictReader(file_input, delimiter=',')
                return list(reader)
            except UnicodeDecodeError:
                continue
        raise UserError(_("Unable to decode the file. Please check the file encoding."))

    def _parse_datetime(self, date_string):
        """
        Parse date from string format to datetime
        """
        if not date_string:
            return False
        
        date_formats = [
            '%m/%d/%Y %H:%M',  # Format in your CSV: 9/21/2024 8:39
            '%m/%d/%Y',
            '%d/%m/%Y %H:%M',
            '%d/%m/%Y',
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d %H:%M',
            '%Y-%m-%d',
        ]

        for fmt in date_formats:
            try:
                return datetime.strptime(date_string.strip(), fmt)
            except ValueError:
                continue
    
        _logger.warning(f"Unable to parse date: {date_string}")
        return False

    def _parse_float(self, value):
        if not value:
            return 0.0
        try:
            # Menghapus pemisah ribuan dan mengganti pemisah desimal
            cleaned_value = value.replace('.', '').replace(',', '.')
            return float(cleaned_value)
        except ValueError:
            _logger.warning(f"Invalid float value: {value}")
            return 0.0

    def _get_or_create_partner(self, row):
        """
        Get or create partner based on username
        """
        Partner = self.env['res.partner']
        username = row.get('Username (Pembeli)')
        
        if not username:
            raise ValidationError(_("Username (Pembeli) is required to create or find a partner."))
        
        partner = Partner.search([('name', '=', username)], limit=1)
        if not partner:
            partner_vals = {
                'name': username,
                'phone': row.get('No. Telepon'),
                'street': row.get('Alamat Pengiriman'),
                'city': row.get('Kota/Kabupaten'),
                'state_id': self._get_state_id(row.get('Provinsi')),
            }
            partner = Partner.create(partner_vals)
        return partner

    def _get_state_id(self, state_name):
        """
        Get state ID based on name
        """
        State = self.env['res.country.state']
        state = State.search([('name', '=', state_name)], limit=1)
        return state.id if state else False

    def _get_or_create_product(self, row):
        """
        Get or create product based on SKU
        """
        Product = self.env['product.product']
        product = Product.search([('default_code', '=', row.get('Nomor Referensi SKU'))], limit=1)
        if not product:
            product = Product.create({
                'name': row.get('Nama Produk'),
                'default_code': row.get('Nomor Referensi SKU'),
                'list_price': self._parse_float(row.get('Harga Awal')),
                'weight': self._parse_float(row.get('Berat Produk')),
            })
        return product

    def _get_or_create_carrier(self, carrier_name):
        """
        Get or create delivery carrier based on name
        """
        Carrier = self.env['delivery.carrier']
        
        if not carrier_name:
            return False
        
        carrier = Carrier.search([('name', '=', carrier_name)], limit=1)
        if not carrier:
            carrier_vals = {
                'name': carrier_name,
                'delivery_type': 'fixed',  # Anda bisa menyesuaikan tipe delivery sesuai kebutuhan
                'product_id': self.env.ref('delivery.product_product_delivery').id,
            }
            carrier = Carrier.create(carrier_vals)
        return carrier    
    
    def _create_sale_order(self, row):
        """
        Create or update sale order based on CSV row data
        """
        SaleOrder = self.env['sale.order']
        order = SaleOrder.search([('nomor_pesanan', '=', row.get('No. Pesanan'))], limit=1)

        partner = self._get_or_create_partner(row)
        carrier = self._get_or_create_carrier(row.get('Opsi Pengiriman'))
        
        order_vals = {
            'partner_id': partner.id,
            'nomor_pesanan': row.get('No. Pesanan'),
            'order_status': row.get('Status Pesanan'),
            'cancellation_return_status': row.get('Status Pembatalan/ Pengembalian'),
            'tracking_number': row.get('No. Resi'),
            'opsi_pengiriman': row.get('Opsi Pengiriman'),
            'carrier_id': carrier.id if carrier else False,
            'shipping_option': 'antar counter' if row.get('Antar ke counter/ pick-up') == 'Antar Ke Counter' else 'pickup',
            'must_ship_before': self._parse_datetime(row.get('Pesanan Harus Dikirimkan Sebelum (Menghindari keterlambatan)')),
            'order_creation_time': self._parse_datetime(row.get('Waktu Pesanan Dibuat')),
            'payment_time': self._parse_datetime(row.get('Waktu Pembayaran Dilakukan')),
            'payment_method': row.get('Metode Pembayaran'),
            'platform_discount': self._parse_float(row.get('Diskon Dari Shopee')),
            'cashback': self._parse_float(row.get('Cashback Koin')),
            'voucher_platform': self._parse_float(row.get('Voucher Ditanggung Shopee')),
            'package_discount': self._parse_float(row.get('Paket Diskon')),
            'package_discount_platform': self._parse_float(row.get('Paket Diskon (Diskon dari Shopee)')),
            'package_discount_seller': self._parse_float(row.get('Paket Diskon (Diskon dari Penjual)')),
            'coin_discount': self._parse_float(row.get('Potongan Koin Shopee')),
            'credit_card_discount': self._parse_float(row.get('Diskon Kartu Kredit')),
            'shipping_fee_paid_by_buyer': self._parse_float(row.get('Ongkos Kirim Dibayar oleh Pembeli')),
            'shipping_fee_discount': self._parse_float(row.get('Estimasi Potongan Biaya Pengiriman')),
            'return_shipping_fee': self._parse_float(row.get('Ongkos Kirim Pengembalian Barang')),
            'estimated_shipping_fee': self._parse_float(row.get('Perkiraan Ongkos Kirim')),
            'buyer_note': row.get('Catatan dari Pembeli'),
            'buyer_username': row.get('Username (Pembeli)'),
            'receiver_name': row.get('Nama Penerima'),
            'receiver_phone': row.get('No. Telepon'),
            'shipping_address': row.get('Alamat Pengiriman'),
            'city': row.get('Kota/Kabupaten'),
            'province': row.get('Provinsi'),
            'order_completion_time': self._parse_datetime(row.get('Waktu Pesanan Selesai')),
        }

        if order:
            order.write(order_vals)
        else:
            order = SaleOrder.create(order_vals)

        # Process order lines
        product = self._get_or_create_product(row)
        
        # Parse values from CSV
        original_price = self._parse_float(row.get('Harga Awal'))
        discounted_price = self._parse_float(row.get('Harga Setelah Diskon'))
        quantity = self._parse_float(row.get('Jumlah'))

        # Calculate discount percentage
        if original_price > 0:
            discount_percentage = ((original_price - discounted_price) / original_price) * 100
        else:
            discount_percentage = 0.0

        line_vals = {
            'order_id': order.id,
            'product_id': product.id,
            'parent_sku': row.get('SKU Induk'),
            'sku_reference': row.get('Nomor Referensi SKU'),
            'variation_name': row.get('Nama Variasi'),
            'original_price': original_price,
            'discounted_price': discounted_price,
            'returned_quantity': self._parse_float(row.get('Returned quantity', '0')),
            'product_uom_qty': quantity,
            'product_weight': self._parse_float(row.get('Berat Produk')),
            'total_weight': self._parse_float(row.get('Total Berat')),
            'discount': discount_percentage,
            'price_unit': original_price,  # Set price_unit directly to original_price
        }
        order.order_line = [(0, 0, line_vals)]

        return order
        
    def import_sales(self):
        """Import sales from the uploaded CSV file."""

        self.ensure_one()
        if not self.file_data:
            raise UserError(_("Please upload a file to import."))

        rows = self._parse_file()
        created_orders = self.env['sale.order']
        errors = []

        for index, row in enumerate(rows, start=1):
            try:
                order = self._create_sale_order(row)
                created_orders |= order
            except ValidationError as e:
                errors.append(f"Row {index}: Validation error - {str(e)}")
            except Exception as e:
                errors.append(f"Row {index}: Unexpected error - {str(e)}")
                _logger.exception("Error importing row %s: %s", index, str(e))
        
        if errors:
            raise UserError("\n".join(errors))
    
        return {
            'type': 'ir.actions.act_window',
            'name': _('Imported Sales Orders'),
            'res_model': 'sale.order',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', created_orders.ids)],
            'context': {'create': False},
        }