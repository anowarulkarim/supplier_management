from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
import xlsxwriter
from io import BytesIO
from base64 import b64decode
from PIL import Image
import io
import base64

class RFPReport(models.TransientModel):
    _name = 'rfp.report'
    _description = 'RFP Report'

    supplier_id = fields.Many2one('res.partner', string='Supplier', required=True, domain=[('supplier_rank', '>', -1)])
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    html_preview = fields.Html(string='HTML Preview', readonly=True)
    report_file = fields.Binary(string="Report File")
    report_file_name = fields.Char(string="Report File Name")

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("Start date must be less than or equal to the end date.")

    def action_generate_html_preview(self):
        rfps = self.env['rfp.request'].search([
            ('approved_supplier_id', '=', self.supplier_id.id),
            ('status', '=', 'accepted'),
            ('required_date', '>=', self.start_date),
            ('required_date', '<=', self.end_date)
        ])
        if not rfps:
            raise UserError("The selected supplier does not have any accepted RFPs in the specified date range.")
        if not self.env.company.logo:
            raise UserError("Please add a logo for the current company.")


        # for rfp in rfps:
        #     print(rfp.rfq_lines)
            # for line in rfp.rfq_lines:
            #     print(line)
            #     # for rfq in line.orde_line:
            #     # # print(line.product_id.name)
            #     # # print(line.product_qty)
            #     # # print(line.price_unit)
            #     #     print(rfq)


        products = self.env['purchase.order'].search([
            ('state', '=', 'purchase'),
            ('rfp_id.approved_supplier_id', '=', self.supplier_id.id),
            ('rfp_id.required_date', '>=', self.start_date),
            ('rfp_id.required_date', '<=', self.end_date),
            ('rfp_id.status','=','accepted'),
        ])

        print(products)

        # for purchase in products:  # Loop through purchase orders
        #     print("rfp id  ",purchase.rfp_id.rfp_number)
        #     for line in purchase.order_line:  # Loop through order lines
                
        #         print(line.product_qty)
        #         print(line.price_unit)
        #         print(line.delivery_charge)
        #         print(line)

        # Prepare data for the template
        data = {
            'rfps': rfps,
            'supplier': self.supplier_id,
            'company': self.env.company,
            'products': products,
        }

        # Render the HTML template
        html_content = self.env['ir.qweb']._render('supplier_management.rfp_report_html_preview_template', data)

        # Update the html_preview field
        self.html_preview = html_content

        # Return an action to reload the form view
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'rfp.report',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'inline',
        }

    def action_generate_excel_report(self):
        if self.start_date > self.end_date:
            raise UserError("The start date must be less than or equal to the end date.")

        rfps = self.env['rfp.request'].search([
            ('approved_supplier_id', '=', self.supplier_id.id),
            ('status', '=', 'accepted'),
            ('required_date', '>=', self.start_date),
            ('required_date', '<=', self.end_date)
        ])
        if not rfps:
            raise UserError("The selected supplier does not have any accepted RFPs in the specified date range.")
        if not self.env.company.logo:
            raise UserError("Please add a logo for the current company.")

        products = self.env['purchase.order.line'].read_group([
            ('order_id.state', '=', 'purchase'),
            ('order_id.rfp_id.approved_supplier_id', '=', self.supplier_id.id),
            ('order_id.rfp_id.required_date', '>=', self.start_date),
            ('order_id.rfp_id.required_date', '<=', self.end_date),
            ('order_id.rfp_id.status', '=', 'accepted')
        ], ['product_id', 'product_qty', 'price_unit', 'delivery_charge', 'price_subtotal'], ['product_id'])

        bank_account = self.supplier_id.bank_ids[:1]  # Fetch first bank account
        bank_name = self.supplier_id.bank_ids[0].bank_name if bank_account.bank_id else "N/A"
        acc_name = self.supplier_id.bank_ids[0].acc_holder_name if bank_account else "N/A"
        acc_number = self.supplier_id.bank_ids[0].acc_number if bank_account else "N/A"
        iban = self.supplier_id.bank_ids[0].bank_id.iban if bank_account else "N/A"
        swift = self.supplier_id.bank_ids[0].bank_bic if bank_account else "N/A"

        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('RFP Report')

        # Add logo
        logo_data = base64.b64decode(self.env.company.logo)
        logo_stream = io.BytesIO(logo_data)
        worksheet.insert_image(0, 0, "logo.png", {'image_data': logo_stream, 'x_scale': 0.5, 'y_scale': 0.5})

        # Define formats
        title_format = workbook.add_format({
            'bold': True,
            'font_size': 16,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#4F81BD',
            'font_color': '#FFFFFF',
            'border': 1
        })
        header_format = workbook.add_format({
            'bold': True,
            'font_size': 12,
            'bg_color': '#D3D3D3',
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'
        })
        cell_format = workbook.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'
        })
        total_format = workbook.add_format({
            'bold': True,
            'bg_color': '#FFD700',
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'
        })
        currency_format = workbook.add_format({
            'num_format': '#,##0.00',
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'
        })

        # Write title
        worksheet.merge_range(5, 7, 5, 4, f"RFP Report for {self.supplier_id.name}", title_format)

        # Write supplier information
        supplier_info = [
            ['Email', self.supplier_id.email],
            ['Phone', self.supplier_id.phone],
            ['Address', self.supplier_id.street],
            ['TIN', self.supplier_id.vat],
            ['Bank Name', bank_name],
            ['Account Name', acc_name],
            ['Account Number', acc_number],
            ['IBAN', iban],
            ['SWIFT', swift],
        ]
        col_offset=5
        row = 7
        for label, value in supplier_info:
            worksheet.write(row, col_offset, label, header_format)
            worksheet.write(row, col_offset+1, value, cell_format)
            row += 1

        row += 2

        # Write RFP table headers
        worksheet.write(row, 0, "RFP Number", header_format)
        worksheet.write(row, 1, "Date", header_format)
        worksheet.write(row, 2, "Required Date", header_format)
        worksheet.write(row, 3, "Total Amount", header_format)
        row += 1

        # Write RFP data
        total_rfp_amount = 0
        for rfp in rfps:
            worksheet.write(row, 0, rfp.rfp_number, cell_format)
            worksheet.write(row, 1, rfp.create_date.strftime('%d/%m/%Y'), cell_format)
            worksheet.write(row, 2, rfp.required_date.strftime('%d/%m/%Y'), cell_format)
            worksheet.write(row, 3, rfp.total_amount, currency_format)
            total_rfp_amount += rfp.total_amount
            row += 1

        # Write total RFP amount
        worksheet.write(row, 2, "Net Amount", total_format)
        worksheet.write(row, 3, total_rfp_amount, total_format)
        row += 2

        # Write product table headers
        worksheet.write(row, 0, "Product Name", header_format)
        worksheet.write(row, 1, "Total Quantity", header_format)
        worksheet.write(row, 2, "Unit Price", header_format)
        worksheet.write(row, 3, "Delivery Charge", header_format)
        worksheet.write(row, 4, "Subtotal", header_format)
        row += 1

        # Write product data
        total_price = 0
        for product in products:
            worksheet.write(row, 0, product['product_id'][1], cell_format)
            worksheet.write(row, 1, product['product_qty'], cell_format)
            worksheet.write(row, 2, product['price_unit'], currency_format)
            worksheet.write(row, 3, product['delivery_charge'], currency_format)
            worksheet.write(row, 4, product['price_subtotal'], currency_format)
            total_price += product['price_subtotal']
            row += 1

        # Write total product price
        worksheet.write(row, 3, "Total Price", total_format)
        worksheet.write(row, 4, total_price, total_format)
        row += 2

        # Write company information
        worksheet.write(row, 0, f"Company Email: {self.env.company.email}", cell_format)
        worksheet.write(row + 1, 0, f"Company Phone: {self.env.company.phone}", cell_format)
        worksheet.write(row + 2, 0, f"Company Address: {self.env.company.partner_id.contact_address}", cell_format)

        header_format = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'bg_color': '#D9EAD3', 'border': 1})
        cell_format = workbook.add_format({'align': 'left', 'valign': 'vcenter', 'border': 1, 'text_wrap': True})

        # Define the table header
        worksheet.write(row, 0, "Company Info", header_format)
        worksheet.write(row, 1, "Details", header_format)

        # Define the rows for company details with borders
        worksheet.write(row + 1, 0, "Company Email:", cell_format)
        worksheet.write(row + 1, 1, self.env.company.email, cell_format)

        worksheet.write(row + 2, 0, "Company Phone:", cell_format)
        worksheet.write(row + 2, 1, self.env.company.phone, cell_format)

        worksheet.write(row + 3, 0, "Company Address:", cell_format)
        worksheet.write(row + 3, 1, self.env.company.partner_id.contact_address, cell_format)

        # Adjust the column width for better readability
        worksheet.set_column(0, 0, 20)  # Set the width for the first column
        worksheet.set_column(1, 1, 30)  # Set the width for the second column

        # Adjust column widths
        worksheet.set_column(0, 0, 20)
        worksheet.set_column(1, 1, 15)
        worksheet.set_column(2, 2, 15)
        worksheet.set_column(3, 3, 15)
        worksheet.set_column(4, 4, 15)

        workbook.close()
        output.seek(0)
        file_data = base64.b64encode(output.getvalue())
        file_name = f"RFP_Report_{self.supplier_id.name}.xlsx"

        attachment = self.env['ir.attachment'].create({
            'name': file_name,
            'type': 'binary',
            'datas': file_data,
            'store_fname': file_name,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })

        self.report_file = file_data
        self.report_file_name = file_name

        return {
            'type': 'ir.actions.act_url',
            'url': f"/web/content/{attachment.id}?download=true",
            'target': 'self',
        }

