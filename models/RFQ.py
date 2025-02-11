from odoo import models, fields, api, _
from odoo.exceptions import UserError

class RFQ(models.Model):
    _inherit = 'purchase.order'
    _description = 'Request for Quotation'

    # supplier = partner_id
    # Expected delivery date = date_planned
    # Terms and Conditions = notes
    # total proce = amount_total
    # currency_id = currency_id
    warranty_period = fields.Integer(string='Warranty Period (months)', required=True)
    rfp_id = fields.Many2one('rfp.request', string='RFP')  # Corrected field name
    score = fields.Integer(string='Score')
    product_line_ids = fields.One2many('rfp.product.line', 'rfp_id', string='Product Lines')
    recommended = fields.Boolean(string='Recommended', default=False)

    @api.constrains('recommended')
    def _check_unique_recommended(self):
        for record in self:
            if record.recommended:
                existing_recommended = self.search([
                    ('partner_id', '=', record.partner_id.id),
                    ('recommended', '=', True),
                    ('id', '!=', record.id)
                ])
                if existing_recommended:
                    raise UserError(_('A supplier cannot have more than one recommended RFQ line.'))
    
    @api.depends('quantity', 'unit_price')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal_price = line.quantity * line.unit_price
