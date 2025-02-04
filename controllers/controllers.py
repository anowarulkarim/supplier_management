# -*- coding: utf-8 -*-
import random
import datetime
from odoo import http, fields
from odoo.http import request


class SupplierManagement(http.Controller):
    @http.route('/supplier_management/create', auth='public', website=True, methods=['POST'], csrf=False)
    def send_otp(self, **post):
        """Generate OTP and store email in session"""
        email = post.get('email')

        if not email:
            return http.Response('{"status": "error", "message": "Email is required"}', content_type='application/json')

        # Generate OTP
        otp_code = str(random.randint(100000, 999999))
        expiry_time = datetime.datetime.now() + datetime.timedelta(minutes=5)

        # Remove previous OTPs
        request.env['otp.verification'].sudo().search([('email', '=', email)]).unlink()

        # Check if email is blacklisted
        blacklisted_email = request.env['mail.blacklist'].sudo().search([('email', '=', email)], limit=1)
        if blacklisted_email:
            return http.Response('{"status": "error", "message": "Email is blacklisted"}', content_type='application/json')

        # Check if email is already used
        existing_email = request.env['res.partner'].sudo().search([('email', '=', email)], limit=1)
        if existing_email:
            return http.Response('{"status": "error", "message": "Email is already used"}', content_type='application/json')

        # Store OTP in database
        request.env['otp.verification'].sudo().create({
            'email': email,
            'otp': otp_code,
            'expiry_time': expiry_time,
            'verified': False
        })

        # Send OTP via email
        mail_values = {
            'email_to': email,
            'email_from': 'anowarul.karim@bjitacademy.com',
            'subject': "Your OTP Code",
            'body_html': f"""
                <p>Hello,</p>
                <p>Your OTP for verification is: <b>{otp_code}</b></p>
                <p>This OTP is valid for 5 minutes.</p>
                <p>Thank you!</p>
            """
        }
        request.env['mail.mail'].sudo().create(mail_values).send()

        return http.Response('{"status": "success", "message": "OTP has been sent"}', content_type='application/json')

    @http.route('/supplier_management/create', auth='public', website=True, methods=['GET'])
    def get_otp_template(self, **kwargs):
        """Render the OTP form template for user input"""
        return request.render('supplier_management.view_email_input_form', {})

    @http.route('/supplier_management/create/user', auth='public', website=True, methods=['GET','POST'])
    def get_user_info(self, **kw):
        error_list = []
        success_list = []
        if request.httprequest.method == 'POST':
            vals = {}
            keys = [
                'company_name', 'email', 'phone', 'company_registered_address', 'company_alternate_address',
                'company_type_category', 'company_type', 'trade_license_number',
                'tax_identification_number', 'commencement_date', 'expiry_date',
                'contact_person_title', 'contact_email', 'contact_phone', 'contact_address',
                'finance_contact_title', 'finance_contact_email', 'finance_contact_phone', 'finance_contact_address',
                'authorized_person_name', 'authorized_person_email', 'authorized_person_phone', 'authorized_person_address',
                'bank_name', 'bank_address', 'bank_swift_code', 'account_name',
                'account_number', 'iban', 'company_address_as_per_bank', 'client_1_name',
                'client_1_address', 'client_1_contact_email',
                'client_1_contact_phone', 'client_2_name',
                'client_2_contact_email', 'client_2_contact_phone', 'client_3_name',
                'client_3_address', 'client_3_contact_email',
                'client_3_contact_phone', 'client_4_name',
                'client_4_address', 'client_4_contact_email',
                'client_4_contact_phone', 'client_5_name',
                'client_5_address', 'client_5_contact_email',
                'client_5_contact_phone', 
                'certification', 'certificate_number',
                'certifying_body', 'award_date', 'certificate_expiry_date'
            ]
            for key in keys:
                if kw.get(key):
                    vals[key] = kw.get(key)
            # if kw.get('tax_identification_number') and (len(kw.get('tax_identification_number')) != 15 or not kw.get(
            #         'tax_identification_number').isdigit()):
            #     error_list.append("Tax Identification Number Should Be Of 15 Digits And All Digits")
            # if kw.get('trade_license_number') and (len(kw.get('trade_license_number')) != 15 or not kw.get(
            #         'trade_license_number').isdigit()):
            #     error_list.append("Trade License Number Should Be Of 15 Digits And All Digits")
            # if kw.get('expiry_date') and fields.Date.to_date(kw.get('expiry_date')) <= fields.date.today():
            #     error_list.append("Expiry Date Should Be Greater Than Today")
            # if not kw.get('company_name'):
            #     error_list.append("Company Name is mandatory")
            # if not kw.get('email'):
            #     error_list.append("Company Email is mandatory")
            # if kw.get('email'):
            #     already_exists = request.env['res.partner'].sudo().search([('email', '=', kw.get('email'))])
            #     if already_exists:
            #         error_list.append("Company Email Already Exists In the system. Try with another email")
            # if not kw.get('bank_name'):
            #     error_list.append("Bank Name is mandatory")
            # if not kw.get('bank_address'):
            #     error_list.append("Bank Address is mandatory")
            # if not kw.get('accoutn_number'):
            #     error_list.append("Account Number is mandatory")
            # if kw.get('client_1_contact_email') or kw.get('client_1_address') or kw.get('client_1_contact_phone'):
            #     if not kw.get('client_1_name'):
            #         error_list.append("If you input any of the field of phone or address or email then Client 1 Name is mandatory")
            #
            # if kw.get('client_2_contact_email') or kw.get('client_2_address') or kw.get('client_2_contact_phone'):
            #     if not kw.get('client_2_name'):
            #         error_list.append("If you input any of the field of phone or address or email then Client 2 Name is mandatory")
            #
            # if kw.get('client_3_contact_email') or kw.get('client_3_address') or kw.get('client_3_contact_phone'):
            #     if not kw.get('client_3_name'):
            #         error_list.append("If you input any of the field of phone or address or email then Client 3 Name is mandatory")
            #
            # if kw.get('client_4_contact_email') or kw.get('client_4_address') or kw.get('client_4_contact_phone'):
            #     if not kw.get('client_4_name'):
            #         error_list.append("If you input any of the field of phone or address or email then Client 4 Name is mandatory")
            #
            # if kw.get('client_5_contact_email') or kw.get('client_5_address') or kw.get('client_5_contact_phone'):
            #     if not kw.get('client_5_name'):
            #         error_list.append("If you input any of the field of phone or address or email then Client 5 Name is mandatory")


            file_fields = [
                'trade_license_business_registration', 'certificate_of_incorporation', 'certificate_of_good_standing',
                'establishment_card', 'vat_tax_certificate', 'memorandum_of_association',
                'identification_document_for_authorized_person', 'bank_letter_indicating_bank_account',
                'past_2_years_audited_financial_statements', 'other_certifications'
            ]
            max_file_size = 1 * 1024 * 1024  # 1 MB in bytes
            for field in file_fields:
                if kw.get(field) and kw.get(field).content_length > max_file_size:
                    error_list.append(f"{field.replace('_', ' ').title()} file size should not exceed 1 MB")

            file_vals = {}
            for field in file_fields:
                if kw.get(field):
                    file_vals[field] = kw.get(field).read()
            vals['state'] = 'submitted'
            if not error_list:
                new_supplier = request.env['supplier.registration'].sudo().create(vals)
                if new_supplier:
                    success_list.append("Supplier Registered Successfully")
                if file_vals:
                    new_supplier.write(file_vals)
        # self.env.ref('supplier_management.vendor_submission_confirmation').send_mail(new_supplier.id)
                # print("new_supplier", new_supplier.email)
                template = request.env.ref('supplier_management.vendor_submission_confirmation')
                template.sudo().send_mail(new_supplier.id, force_send=True)
        return request.render("supplier_management.new_supplier_registration_form_view_portal",
                              {'page_name': 'supplier_registration',
                               'error_list': error_list,
                               'success_list': success_list})

    @http.route('/supplier_management/verify_otp', auth='public', website=True, methods=['POST'], csrf=False)
    def verify_otp(self, **post):
        """Verify OTP"""
        email = post.get('email')
        otp = post.get('otp')

        if not email or not otp:
            return http.Response('{"status": "error", "message": "Email and OTP are required"}', content_type='application/json')

        otp_record = request.env['otp.verification'].sudo().search([('email', '=', email), ('otp', '=', otp)], limit=1)

        if not otp_record or otp_record.expiry_time < datetime.datetime.now():
            return http.Response('{"status": "error", "message": "Invalid or expired OTP"}', content_type='application/json')

        # Mark OTP as verified
        otp_record.sudo().write({'verified': True})

        # return request.render('supplier_management.user_registration_form',{})

        return http.Response('{"status": "success", "message": "OTP verified successfully"}', content_type='application/json')
