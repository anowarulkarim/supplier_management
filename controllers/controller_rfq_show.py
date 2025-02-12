from odoo import http
from odoo.http import request

class SupplierManagement(http.Controller):

    @http.route('/supplier_management/rfq', type='http', auth='public', website=True)
    def show_rfq(self, **kwargs):
        rfqs = request.env['purchase.order'].search([('partner_id', '=', request.env.user.partner_id.id)])
        print(rfqs)
        return request.render('supplier_management.rfq_list_template', {
            'rfqs': rfqs
        })

    @http.route('/supplier_management/rfq/<int:rfp_id>', auth='user', website=True)
    def show_rfq_details(self, rfp_id):
        # Fetch the specific RFQ based on the ID
        rfp = request.env['purchase.order'].browse(rfp_id)

        # Ensure the RFQ belongs to the logged-in user's partner
        if rfp.partner_id.id != request.env.user.partner_id.id:
            return request.redirect('/supplier_management/rfq')

        # Render the template with the RFQ details
        return request.render('supplier_management.rfq_details_template', {
            'rfp': rfp,
        })