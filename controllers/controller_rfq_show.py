from odoo import http, _  # Import the `_` function for translations
from odoo.http import request
from odoo.addons.portal.controllers.portal import pager as portal_pager  # Import portal_pager
from itertools import groupby


class SupplierManagement(http.Controller):

    @http.route([
        '/supplier_management/rfq',
        '/supplier_management/rfq/page/<int:page>',
    ], type='http', auth='user', website=True)
    def show_rfq(self, page=1, sortby=None, search=None, search_in=None, **kwargs):
        limit = 4  # Number of items per page

        # Define sorting options
        rfps=request.env["purchase.order"].search([('partner_id','=',request.env.user.partner_id.id)])
        

        searchbar_sortings = {
            'rfp_id': {'label': _('RFQ Number'), 'order': 'rfp_id'},
        }

        if not search_in:
            search_in = 'rfp_id'

        # Get the sort order
        order = searchbar_sortings[sortby]['order'] if sortby else 'rfp_id'
        if not sortby:
            sortby = 'rfp_id'

        # Define search filters
        search_list = {
            'all': {'label': _('All'), 'input': 'all', 'domain': []},
            'total_number': {'label': _('RFP Number'), 'input': 'rfp_id', 'domain': [('rfp_id.rfp_number', 'ilike', search)]},
        }

        # Build the search domain based on the provided search term
        search_domain = []
        if search:
            # search_domain += search_list[search_in]['domain']
            search_domain += [('rfp_id.rfp_number', 'ilike', search)]


        # Filter records to show only approved RFPs
        search_domain += [('state', '=', 'purchase')]

        # Count the number of RFP records matching the domain
        rfp_count = request.env['purchase.order'].sudo().search_count(search_domain)

        # Setup pagination
        pager = portal_pager(
            url='/supplier_management/rfq',
            url_args={'sortby': sortby, 'search_in': search_in, 'search': search},
            total=rfp_count,
            page=page,
            step=limit,
        )

        # Search for RFP records based on the domain, pagination, and order
        combined_domain = [('partner_id', '=', request.env.user.partner_id.id)] + search_domain

        # Search for RFPs using the combined domain
        rfps = request.env['purchase.order'].sudo().search(
            combined_domain, limit=limit, offset=pager['offset'], order=order
        )
        
        return request.render('supplier_management.rfq_list_template', {
            'page_name': 'rfq_list',
            'pager': pager,
            'sortby': sortby,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_inputs': search_list,
            'search_in': search_in,
            'search': search,
            # 'rfp_groups': rfp_group_list,
            'default_url': '/supplier_management/rfq',
            # 'searchbar_groupby': groupby_list,
            'rfqs': rfps,
        })


    

    @http.route('/supplier_management/rfq/<int:rfp_id>', auth='user', website=True)
    def show_rfq_details(self, rfp_id):
        # Fetch the specific RFQ based on the ID
        rfp = request.env['purchase.order'].sudo().browse(rfp_id)

        # Ensure the RFQ belongs to the logged-in user's partner
        if rfp.partner_id.id != request.env.user.partner_id.id:
            return request.redirect('/supplier_management/rfq')

        # Render the template with the RFQ details
        return request.render('supplier_management.rfq_details_template', {
            'rfp': rfp,
        })