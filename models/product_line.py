from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ProductLine(models.Model):
    _name = 'rfp.product.line'
    _description = 'RFP Product Line'

    rfp_id = fields.Many2one('rfp.request', string='RFP')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    description = fields.Text(string='Description')
    quantity = fields.Integer(string='Quantity', required=True, default=1)
    unit_price = fields.Monetary(string='Unit Price', currency_field='currency_id')
    subtotal_price = fields.Monetary(string='Subtotal Price', compute='_compute_subtotal', store=True)
    delivery_charges = fields.Monetary(string='Delivery Charges')
    currency_id = fields.Many2one('res.currency', related='rfp_id.currency_id', store=True)

    @api.depends('quantity', 'unit_price')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal_price = line.quantity * line.unit_price