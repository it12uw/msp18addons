from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class InMarelKodeDokumenSuratJalan(models.Model):
    _inherit = 'stock.picking'
    
    tgl_kirim = fields.Date(string=u'Tgl Kirim',store=True)

class MarelInStockMove(models.Model):
    _inherit = 'stock.move'
    
    keterangan_move = fields.Text(string=u'Keterangan',store=True)
    rb= fields.Integer(string=u'RB',store=True)
    rk= fields.Integer(string=u'RK',store=True)
    rijek= fields.Integer(string=u'Rijek',store=True)
    noorder = fields.Char('No Order',store=True)
    

class MarelInStockMove(models.Model):
    _inherit = 'stock.move.line'
    
    keterangan_move_line = fields.Text(string=u'Keterangan',store=True)


class InheritSalesOrder(models.Model):
    _inherit = 'sale.order'

    created_uid = fields.Many2one('res.users', string='Created By')
    supervise_uid = fields.Many2one('res.users', string='Supervised By')
    supervise_uid_2 = fields.Many2one('res.users', string='Supervised By 2')   