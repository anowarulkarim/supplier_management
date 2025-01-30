from odoo import models, fields

class OTPVerification(models.Model):
    _name = "otp.verification"
    _description = "OTP Verification"

    email = fields.Char(string="Email", required=True)
    otp = fields.Char(string="OTP", required=True)
    expiry_time = fields.Datetime(string="Expiry Time", required=True)
    verified = fields.Boolean(string="Verified", default=False)



