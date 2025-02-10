from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ProductOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    _description = 'Product Order Line'

    # product_id = product_id
    # product_qty = product_qty
    # price_unit = price_unit
    # product_uom = product_uom
    # date_planned = date_planned
    # order_id = order_id
    # currency_id = currency

    delivery_charge = fields.Float(string='Delivery Charge', default=0.0)

    # @api.onchange('product_qty', 'price_unit')
    # def _onchange_product_qty_price_unit(self):
    #     if self.product_qty and self.price_unit:
    #         self.delivery_charge = self.product_qty * 0.05  # Example calculation

    @api.depends('product_qty', 'price_unit', 'taxes_id', 'discount','delivery_charge')
    def _compute_amount(self):
        for line in self:
            tax_results = self.env['account.tax']._compute_taxes([line._convert_to_tax_base_line_dict()])
            totals = next(iter(tax_results['totals'].values()))
            amount_untaxed = totals['amount_untaxed']
            if line.delivery_charge:
                amount_untaxed = amount_untaxed + line.delivery_charge
                # totals = totals+line.delivery_charge
            amount_tax = totals['amount_tax']

            line.update({
                'price_subtotal': amount_untaxed,
                'price_tax': amount_tax,
                'price_total': amount_untaxed + amount_tax + line.delivery_charge,
            })