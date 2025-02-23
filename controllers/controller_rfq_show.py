from odoo import http, _  # Import the `_` function for translations
from odoo.http import request
from odoo.addons.portal.controllers.portal import pager as portal_pager  # Import portal_pager
from itertools import groupby


class SupplierManagement(http.Controller):

    @http.route([
        '/supplier_management/rfq',
        '/supplier_management/rfq/page/<int:page>',
    ], type='http', auth='public', website=True)
    def show_rfq(self, page=1, sortby=None, search=None, search_in=None, groupby=None, **kwargs):
        limit = 4  # Number of items per page

        # Define sorting options
        rfps=request.env["purchase.order"].search([('partner_id','=',request.env.user.partner_id.id)])
        print(rfps)
        searchbar_sortings = {
            'rfp_id': {'label': _('RFP Number'), 'order': 'rfp_id'},
            'required_date': {'label': _('Required Date'), 'order': 'required_date'},
        }

        # Define grouping options
        # groupby_list = {
        #     'required_date': {'input': 'required_date', 'label': _('Required Date')},
        # }

        # Default groupby if not provided
        # if not groupby:
        #     groupby = 'required_date'

        # group_by_rfp = groupby_list.get(groupby, {})

        # Default search field is 'rfp_id'
        if not search_in:
            search_in = 'rfp_id'

        # Get the sort order
        order = searchbar_sortings[sortby]['order'] if sortby else 'rfp_id'
        if not sortby:
            sortby = 'rfp_id'

        # Define search filters
        search_list = {
            'all': {'label': _('All'), 'input': 'all', 'domain': []},
            'rfp_id': {'label': _('RFP Number'), 'input': 'rfp_id', 'domain': [('rfp_id', 'ilike', search)]},
            'required_date': {'label': _('Required Date'), 'input': 'required_date', 'domain': [('required_date', '=', search)]},
        }

        # Build the search domain based on the provided search term
        search_domain = []
        if search:
            search_domain += search_list[search_in]['domain']

        # Filter records to show only approved RFPs
        search_domain.append(('status', '=', 'approved'))
        search_domain.append(('status', '!=', 'closed'))

        # Count the number of RFP records matching the domain
        rfp_count = request.env['rfp.request'].sudo().search_count(search_domain)

        # Setup pagination
        pager = portal_pager(
            url='/supplier_management/rfq',
            url_args={'sortby': sortby, 'search_in': search_in, 'search': search, 'groupby': groupby},
            total=rfp_count,
            page=page,
            step=limit,
        )

        # Search for RFP records based on the domain, pagination, and order
        rfps = request.env['purchase.order'].sudo().search(
            [('partner_id','=',request.env.user.partner_id.id)], limit=limit, offset=pager['offset'], order=order
        )

        # Group the RFPs according to the selected grouping option
        # if groupby_list.get(groupby) and groupby_list[groupby]['input']:
        #     # Sort the RFPs by the grouping key
        #     rfps_sorted = sorted(rfps, key=lambda r: getattr(r, group_by_rfp['input']))
        #     # Group the sorted RFPs
        #     rfp_group_list = [
        #         {
        #             'group_name': key,
        #             'rfps': list(group)
        #         }
        #         for key, group in groupby(rfps_sorted, key=lambda r: getattr(r, group_by_rfp['input']))
        #     ]
        # else:
        #     rfp_group_list = [{'group_name': _('All RFPs'), 'rfps': rfps}]

        # Render the portal view template with the prepared values
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
            'groupby': groupby,
            # 'searchbar_groupby': groupby_list,
            'rfps': rfps,
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