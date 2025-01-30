from odoo import http, fields
from odoo.http import request
import json


class AuthController(http.Controller):



    @http.route('/api/send_otp', type='json', auth='public', methods=['POST'], csrf=False)
    def send_otp(self, **post):
        """Send OTP for email verification."""
        email = post.get('email')
        if not email:
            return {'error': 'Email is required'}

        # Check if email is already registered
        existing_user = request.env['res.partner'].sudo().search([('email', '=', email)])
        blacklisted = request.env['otp.verification'].sudo().search([('email', '=', email), ('blacklisted', '=', True)])

        if existing_user:
            return {'error': 'Email is already registered'}
        if blacklisted:
            return {'error': 'Email is blacklisted'}

        # Generate OTP
        otp_record = request.env['otp.verification'].sudo().generate_otp(email)

        # Send OTP email
        request.env['mail.template'].sudo().send_otp_email(email, otp_record.otp)

        return {'success': 'OTP has been sent to your email'}

    @http.route('/api/verify_otp', type='json', auth='public', methods=['POST'], csrf=False)
    def verify_otp(self, **post):
        """Verify OTP and allow registration."""
        email = post.get('email')
        otp = post.get('otp')

        if not email or not otp:
            return {'error': 'Email and OTP are required'}

        otp_record = request.env['otp.verification'].sudo().search([
            ('email', '=', email), ('otp', '=', otp), ('verified', '=', False)
        ])

        if not otp_record:
            return {'error': 'Invalid OTP'}

        if otp_record.expiry_time < fields.Datetime.now():
            return {'error': 'OTP has expired'}

        # Mark OTP as verified
        otp_record.sudo().write({'verified': True})
        return {'success': 'OTP verified. Proceeding to registration'}
