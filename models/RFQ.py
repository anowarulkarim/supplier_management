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
    product_line_ids = fields.One2many('rfp.product.line', 'rfp_id', string='Product Lines' )
    recommended = fields.Boolean(string='Recommended', default=False)
    rfp_state = fields.Selection(related='rfp_id.status', string='RFP status')

    @api.constrains('recommended')
    def _check_unique_recommended(self):
        for record in self:
            if record.recommended:
                existing_recommended = self.search([
                    ('rfp_id','=', record.rfp_id.id),
                    ('partner_id', '=', record.partner_id.id),
                    ('recommended', '=', True),
                    ('id', '!=', record.id)
                ])
                if existing_recommended:
                    raise UserError(_('A supplier cannot have more than one recommended RFQ line.'))

    @api.onchange('score')
    def _onchange_score(self):
        for record in self:
            if record.score < 0 or record.score > 10:
                raise UserError(_('Score must be in 0-10'))
    
    def confirm_rfq(self):
        # self.rfp_state = 'accepted'
        self.rfp_id.write({'status': 'accepted'})
        self.state='purchase'
        self.rfp_id.approved_supplier_id = self.partner_id
        self.rfp_id.write({'total_amount': self.amount_total})
        template = self.env.ref('supplier_management.rfq_accepted_supplier')
        if template:
            email_values = {
                'email_to': self.partner_id.email,
                # 'email_from': self.env.user.email,
                'email_from': 'anowarul.karim@bjitacademy.com',
            }
            ctx = {
                'rfq': self,
                'rfp': self.rfp_id,
                'rfq_number': self.rfp_id.rfp_number,
            }
            template.with_context(**ctx).send_mail(self.id, email_values=email_values)

        


    @api.depends('quantity', 'unit_price')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal_price = line.quantity * line.unit_price
