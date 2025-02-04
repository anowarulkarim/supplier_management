from odoo import models, fields

class RejectReasonWizard(models.TransientModel):
    _name = 'reject.reason.wizard'
    _description = 'Wizard for Rejecting'

    reason = fields.Text(string="Rejection Reason", required=True)

    def action_submit_reason(self):
        """Handles the submission of the rejection reason"""
        active_id = self.env.context.get('active_id')
        if active_id:
            record = self.env['supplier.registration'].browse(active_id)
            record.write({'state': 'rejected', 'reject_reason': self.reason})
        return {'type': 'ir.actions.act_window_close'}