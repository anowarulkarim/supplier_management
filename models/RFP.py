from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import timedelta

class RFP(models.Model):
    _name = 'rfp.request'
    _description = 'Request for Purchase'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='RFP Number', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    status = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('closed', 'Closed'),
        ('recommendation', 'Recommendation'),
        ('accepted', 'Accepted')
    ], string='Status', default='draft', tracking=True)
    required_date = fields.Date(string='Required Date', default=lambda self: fields.Date.today() + timedelta(days=7))
    total_amount = fields.Monetary(string='Total Amount', compute='_compute_total_amount', store=True,currency_field='currency_id')
    approved_supplier_id = fields.Many2one('res.partner', string='Approved Supplier')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    product_line_ids = fields.One2many('rfp.product.line', 'rfp_id', string='Product Lines')
    rfq_lines = fields.One2many('purchase.order', 'rfp_id', string='RFQ Lines')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('rfp.request') or _('New')
        return super().create(vals)

    @api.depends('rfq_lines.amount_total')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(record.rfq_lines.mapped('amount_total'))

    def action_submit(self):
        if self.status != 'draft':
            raise UserError(_('Only Draft RFPs can be submitted.'))
        self.status = 'submitted'
        self.message_post(body=_('RFP has been submitted.'))

    def action_return_to_draft(self):
        if self.status != 'submitted':
            raise UserError(_('Only Submitted RFPs can be returned to draft.'))
        self.status = 'draft'
        self.message_post(body=_('RFP has been moved back to Draft.'))

    def action_approve(self):
        if self.status != 'submitted':
            raise UserError(_('Only Submitted RFPs can be approved.'))
        self.status = 'approved'
        self.message_post(body=_('RFP has been approved.'))

    def action_reject(self):
        if self.status != 'submitted':
            raise UserError(_('Only Submitted RFPs can be rejected.'))
        self.status = 'rejected'
        self.message_post(body=_('RFP has been rejected.'))

    def action_close(self):
        if self.status != 'approved':
            raise UserError(_('Only Approved RFPs can be closed.'))
        self.status = 'closed'
        self.message_post(body=_('RFP has been closed.'))

    def action_accept(self):
        if self.status != 'recommendation':
            raise UserError(_('Only Recommended RFPs can be accepted.'))
        self.status = 'accepted'
        self.message_post(body=_('RFP has been accepted.'))



