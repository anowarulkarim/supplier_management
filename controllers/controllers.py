# -*- coding: utf-8 -*-
import random
import datetime
from odoo import http, fields, _
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.http import request
from math import ceil
from itertools import groupby as groupbyelem


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
        print("OTP Code:", otp_code)

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
        # Store email in session


        return http.Response('{"status": "success", "message": "OTP has been sent"}', content_type='application/json')

    @http.route('/supplier_management/create', auth='public', website=True, methods=['GET'])
    def get_otp_template(self, **kwargs):
        """Render the OTP form template for user input"""
        return request.render('supplier_management.view_email_input_form', {})

    @http.route('/supplier_management/create/user', auth='public', website=True, methods=['GET','POST'])
    def get_user_info(self, **kw):
        error_list = []
        success_list = []
        # Check if OTP email is in session
        if 'otp_email' not in request.session:
            return request.redirect('/supplier_management/create')
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
                'past_2_years_audited_financial_statements', 'other_certifications','image_1920'
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

                template = request.env.ref('supplier_management.reviewer_notification_email')

                if not template:
                    return {"error": "Email template not found!"}
                reviewer = request.env['res.groups'].search([('name', '=', 'Reviewer')])
                reviewer_user = reviewer.users
                for user in reviewer_user:
                    # template.with_context(user=user).send_mail(user.id, force_send=True)
                    print(user.email)
                    template.with_context(email_to=user.email).send_mail(user.id, force_send=True)
                    # raise RuntimeError("Intentional error raised!")







                    # user.partner_id.notify_info(message="New Supplier Registration Request has been submitted")
                # template = request.env.ref('supplier_management.vendor_submission_confirmation')
                # print("template", template)
                # if template:
                #     try:
                #         print("Attempting to send mail...")

                #         # Add context with force_send to ensure immediate email sending
                #         ctx = {
                #             'default_model': 'supplier.registration',
                #             'default_res_id': new_supplier.id,
                #             'default_email_to': new_supplier.email,  # Ensure the email field exists
                #             'default_template_id': template.id,
                #             'force_send': True,
                #         }

                #         s = template.with_context(**ctx).send_mail(new_supplier.id, force_send=True)
                #         print("Email Sent, ID:", s)
                #     except Exception as e:
                #         print("Error in send_mail:", str(e))

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
        request.session['otp_email'] = email
        # return request.render('supplier_management.user_registration_form',{})

        return http.Response('{"status": "success", "message": "OTP verified successfully"}', content_type='application/json')

    @http.route(['/supplier_management/rfp', '/supplier_management/rfp/page/<int:page>'], auth='public', website=True)
    def portal_rfp_list(self, page=1, sortby=None, search=None, search_in=None, groupby='required_date', **kw):
        limit = 4

        # Define sorting options
        searchbar_sortings = {
            'rfp_number': {'label': _('RFP Number'), 'order': 'rfp_number'},
            'required_date': {'label': _('Required Date'), 'order': 'required_date'},
        }

        # Define grouping options (status grouping removed since all RFPs are approved)
        groupby_list = {
            'required_date': {'input': 'required_date', 'label': _('Required Date')},
        }
        group_by_rfp = groupby_list.get(groupby, {})

        # Default search field is 'name'
        if not search_in:
            search_in = 'rfp_number'

        # Get the sort order
        order = searchbar_sortings[sortby]['order'] if sortby else 'rfp_number'
        if not sortby:
            sortby = 'rfp_number'

        # Define search filters (removed the status option)
        search_list = {
            'all': {'label': _('All'), 'input': 'all', 'domain': []},
            'rfp_number': {'label': _('RFP Number'), 'input': 'rfp_number', 'domain': [('rfp_number', 'ilike', search)]},
            'required_date': {'label': _('Required Date'), 'input': 'required_date',
                              'domain': [('required_date', '=', search)]},
        }

        # Build the search domain based on the provided search term
        search_domain = []
        if search:
            search_domain += search_list[search_in]['domain']

        # Filter records to show only approved RFPs
        search_domain.append(('status', '=', 'approved'))

        # Count the number of RFP records matching the domain
        rfp_count = request.env['rfp.request'].sudo().search_count(search_domain)

        # Setup pagination
        pager = portal_pager(
            url='/supplier_management/rfp',
            url_args={'sortby': sortby, 'search_in': search_in, 'search': search},
            total=rfp_count,
            page=page,
            step=limit,
        )

        # Search for RFP records based on the domain, pagination, and order
        rfps = request.env['rfp.request'].sudo().search(
            search_domain, limit=limit, offset=pager['offset'], order=order
        )

        # Group the RFPs according to the selected grouping option (only required_date remains)
        if groupby_list.get(groupby) and groupby_list[groupby]['input']:
            rfp_group_list = [
                {
                    'group_name': key.rfp_number if hasattr(key, 'rfp_number') else key,
                    'rfps': list(group)
                }
                for key, group in groupbyelem(rfps, key=lambda r: getattr(r, group_by_rfp['input']))
            ]
        else:
            rfp_group_list = [{'group_name': _('All RFPs'), 'rfps': rfps}]
        # print(rfp_group_list[0]['rfps'])

        # Render the portal view template with the prepared values
        return request.render('supplier_management.rfp_list_template', {
            'page_name': 'rfp_list',
            'pager': pager,
            'sortby': sortby,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_inputs': search_list,
            'search_in': search_in,
            'search': search,
            'rfp_groups': rfp_group_list,
            'default_url': 'supplier_management/rfp',
            'groupby': groupby,
            'searchbar_groupby': groupby_list,
            'rfps' : rfps,
        })


    @http.route('/supplier_management/rfp/<int:rfp_id>', auth='public', website=True, methods=['GET'])
    def view_rfp_details(self, rfp_id, **kwargs):
        """Show details of a specific RFP and allow RFQ creation"""
        rfp = request.env['rfp.request'].sudo().browse(rfp_id)
        if not rfp.exists():
            return request.not_found()

        return request.render('supplier_management.rfp_detail_template', {'rfp': rfp})

    # @http.route('/supplier_management/rfp/<int:rfp_id>/create_rfq', auth='public', website=True, methods=['POST','GET'])
    # def create_rfq(self, rfp_id, **kwargs):
    #     """Create an RFQ for a given RFP"""
    #     rfp = request.env['rfp.request'].sudo().browse(rfp_id)
    #     if not rfp.exists():
    #         return request.not_found()

    #     # Get supplier info from the request
    #     supplier_id = int(kwargs.get('supplier_id', 0))
    #     warranty_period = int(kwargs.get('warranty_period', 0))

    #     if not supplier_id:
    #         return request.render('supplier_management.rfp_detail_template', {
    #             'rfp': rfp,
    #             'error': 'Supplier is required to create an RFQ.'
    #         })

    #     rfq_vals = {
    #         'partner_id': supplier_id,
    #         'rfp_id': rfp.id,
    #         'date_order': fields.Date.today(),
    #         'currency_id': rfp.currency_id.id,
    #         'warranty_period': warranty_period,
    #     }
    #     rfq = request.env['purchase.order'].sudo().create(rfq_vals)

    #     return request.redirect('/supplier_management/rfp/{}'.format(rfp_id))
    @http.route('/supplier_management/rfp/<int:rfp_id>/create_rfq', auth='user', website=True, methods=['GET', 'POST'])
    def create_rfq(self, rfp_id, **kwargs):
        """Handles both GET (display form) and POST (submit RFQ)."""
        rfp = request.env['rfp.request'].sudo().browse(rfp_id)

        if not rfp.exists():
            return request.redirect('/supplier_management/rfp')  # Redirect if RFP doesn't exist

        if http.request.httprequest.method == 'POST':
            # Extract form data
            warranty_period = int(kwargs.get('warranty_period', 0))
            date_planned = kwargs.get('date_planned')
            notes = kwargs.get('notes')

            # Get the current supplier (partner)
            partner_id = request.env.user.partner_id.id

            # Create RFQ (purchase order)
            purchase_order = request.env['purchase.order'].sudo().create({
                'partner_id': partner_id,
                'date_planned': date_planned,
                'notes': notes,
                'rfp_id': rfp_id,
                'warranty_period': warranty_period,
                'currency_id': rfp.currency_id.id,
            })

            # Add the product lines to purchase.order.line
            for line in rfp.product_line_ids:
                # Capture form data for each product line using dynamic field names
                product_qty = int(kwargs.get(f'quantity_{line.id}', 0))
                unit_price = float(kwargs.get(f'unit_price_{line.id}', 0))
                delivery_charges = float(kwargs.get(f'delivery_charges_{line.id}', 0))
                print("asdfjkljasdlfjl     ",delivery_charges,"asdf")
                if kwargs[f'delivery_charges_{line.id}'] == '':
                    delivery_charges = 0

                # Create purchase order line
                request.env['purchase.order.line'].sudo().create({
                    'order_id': purchase_order.id,  # Link the line to the purchase order
                    'product_id': line.product_id.id,
                    'product_qty': product_qty,
                    'price_unit': unit_price,
                    'delivery_charge': delivery_charges,
                    'taxes_id': [(6, 0, [tax.id for tax in line.product_id.supplier_taxes_id])],  # Link taxes
                    'name': "asdfhjk",  # Add description from product line
                })

            # Redirect to success page after RFQ creation
            return request.redirect('/supplier_management/rfq/success')

        # If GET request, render form
        return request.render('supplier_management.rfq_form', {'rfp': rfp})

    @http.route('/supplier_management/rfq/success', type='http', auth="public", website=True)
    def rfq_success(self):
        
        return request.render('supplier_management.rfq_success_template', {})


