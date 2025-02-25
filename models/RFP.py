from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import timedelta

class RFP(models.Model):
    _name = 'rfp.request'
    _description = 'Request for Purchase'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'rfp_number'

    rfp_number = fields.Char(string='RFP Number', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
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
    total_amount = fields.Monetary(string='Total Amount', compute='_compute_total_amount', store=True, currency_field='currency_id')
    approved_supplier_id = fields.Many2one('res.partner', string='Approved Supplier')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    product_line_ids = fields.One2many('rfp.product.line', 'rfp_id', string='Product Lines')
    rfq_lines = fields.One2many('purchase.order', 'rfp_id', string='RFQ Lines', tracking=True,domain=lambda self : self._get_rfq())
    # rfq_lines = fields.One2many('purchase.order', 'rfp_id', string='RFQ Lines', tracking=True)

    @api.model
    def _get_rfq(self):
        if self.env.user.has_group('supplier_management.group_supplier_management_approver'):
            # return [('recommended', '=', True)] if self.status in ['recommendation','accepted' ] else [("id","=",False)]
            if self.status in ['recommendation','accepted','closed']:
                return [('recommended', '=', True)]
            else:
                return [("id","=",False)]
        else:
            return []

    @api.model
    def create(self, vals):
        # self.status='submitted'
        if not vals.get('rfp_number') or vals.get('rfp_number') == _('New'):
            seq_number = self.env['ir.sequence'].next_by_code('serial.number.sequence')  # Match the XML code
            vals['rfp_number'] = seq_number or _('New')
        # vals['status'] = 'submitted'
        return super(RFP, self).create(vals)
    
    # @api.model
    # def create(self, vals):
    #     if not vals.get('rfp_number') or vals.get('rfp_number') == _('New'):
    #         seq_number = self.env['ir.sequence'].next_by_code('serial.number.sequence')
    #         vals['rfp_number'] = seq_number or _('New')
        
    #     return super(RFP, self).create(vals)

    @api.depends('rfq_lines.amount_total')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(record.rfq_lines.mapped('amount_total'))

    def action_submit_rfp(self):
        if self.status != 'draft':
            raise UserError(_('Only Draft RFPs can be submitted.'))
        self.status = 'submitted'
        template = self.env.ref('supplier_management.rfp_review_reviewer')
        if template:
            try:
                
                    # Add context with force_send to ensure immediate email sending
                # approvers=self.env["res.user"].search([("groups.id","in",self.env.ref("group_supplier_management_approver")),])
                approvers = self.env['res.groups'].search([('name', '=', 'Approver')])
                approver_all = approvers.users
                for approver in approver_all:
                    email_values = {
                        'email_to': approver.email,
                        'email_from': 'anowarul.karim@bjitacademy.com'
                    }
                    ctx = {
                        'default_model': 'rfp.request',
                        'default_res_id': self.id,
                        'default_use_template': bool(template),
                        'default_template_id': template.id,
                        'default_composition_mode': 'comment',
                        'force_send': True,
                        'rfp_number': self.rfp_number
                    }
                    template.with_context(**ctx).send_mail(self.id,email_values=email_values)
            except Exception as e:
                pass
        self.message_post(body=_('RFP has been submitted.'))

    def action_return_to_draft_rfp(self):
        if self.status != 'submitted':
            raise UserError(_('Only Submitted RFPs can be returned to draft.'))
        self.status = 'draft'
        self.message_post(body=_('RFP has been moved back to Draft.'))

    def action_approve_rfp(self):
        if self.status != 'submitted':
            raise UserError(_('Only Submitted RFPs can be approved.'))
        self.status = 'approved'
        template = self.env.ref('supplier_management.reviewer_notification_rfp_approved')
        if template:
            try:
                
                    # Add context with force_send to ensure immediate email sending
                email_values = {
                    'email_to': self.create_uid.email,
                    'email_from': 'anowarul.karim@bjitacademy.com'
                }
                ctx = {
                    'default_model': 'rfp.request',
                    'default_res_id': self.id,
                    'default_use_template': bool(template),
                    'default_template_id': template.id,
                    'default_composition_mode': 'comment',
                    'force_send': True,
                    'rfp_number': self.rfp_number
                }
                template.with_context(**ctx).send_mail(self.id, email_values=email_values)

            except Exception as e:
                pass

        template2 = self.env.ref('supplier_management.supplier_notification_new_rfp')
        if template2:
            try:
                
                    # Add context with force_send to ensure immediate email sending

                suppliers = self.env['res.partner'].search([('supplier_rank', '>', 0)])

                for supplier in suppliers:
                    email_values = {
                        'email_to': supplier.email,
                        'email_from': 'anowarul.karim@bjitacademy.com'
                    }
                    ctx = {
                        'default_model': 'rfp.request',
                        'default_res_id': self.id,
                        'default_use_template': bool(template2),
                        'default_template_id': template2.id,
                        'default_composition_mode': 'comment',
                        'force_send': True,
                        'supplier_name': supplier.name,
                        'rfp_number': self.rfp_number,
                    }
                    template2.with_context(**ctx).send_mail(self.id, email_values=email_values)
            except Exception as e:
                pass

        self.message_post(body=_('RFP has been approved.'))

    def action_reject_rfp(self):
        if self.status != 'submitted':
            raise UserError(_('Only Submitted RFPs can be rejected.'))

        template = self.env.ref('supplier_management.rfp_reject')
        if template:
            try:
                
                    # Add context with force_send to ensure immediate email sending
                email_values = {
                    'email_to': self.create_uid.email,
                    'email_from': 'anowarul.karim@bjitacademy.com'
                }
                ctx = {
                    'default_model': 'rfp.request',
                    'default_res_id': self.id,
                    'default_use_template': bool(template),
                    'default_template_id': template.id,
                    'default_composition_mode': 'comment',
                    'name_user': self.create_uid.name,
                    'force_send': True,
                    'rfp_number': self.rfp_number
                }
                template.with_context(**ctx).send_mail(self.id, email_values=email_values)
            except Exception as e:
                pass
        self.status = 'rejected'
        self.message_post(body=_('RFP has been rejected.'))

    def action_close_rfp(self):
        if self.status != 'approved':
            raise UserError(_('Only Approved RFPs can be closed.'))
        self.status = 'closed'
        template = self.env.ref('supplier_management.rfp_closed_notification_reviewer')
        if template:
            try:
                
                    # Add context with force_send to ensure immediate email sending
                email_values = {
                    'email_to': self.create_uid.email,
                    'email_from': 'anowaru.karim@bjitacademy.com'
                }
                ctx ={
                    'default_model': 'rfp.request',
                    'default_res_id': self.id,
                    'default_use_template': bool(template),
                    'default_template_id': template.id,
                    'default_composition_mode': 'comment',
                    'force_send': True,
                    'rfp_number': self.rfp_number
                }
                template.with_context(**ctx).send_mail(self.id, email_values=email_values)
            except Exception as e:
                pass
        self.message_post(body=_('RFP has been closed.'))

    def action_accept_rfp(self):
        if self.status != 'recommendation':
            raise UserError(_('Only Recommended RFPs can be accepted.'))
        self.status = 'accepted'
        self.message_post(body=_('RFP has been accepted.'))
