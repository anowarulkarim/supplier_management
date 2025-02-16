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
            ('partner_id', '=', self.supplier_id.id),
            ('rfp_id.required_date', '>=', self.start_date),
            ('rfp_id.required_date', '<=', self.end_date),
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

        products = self.env['purchase.order'].search([
            ('state', '=', 'purchase'),
            ('partner_id', '=', self.supplier_id.id)
        ])

        # Create an Excel file in memory
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('RFP Report')

        # Retrieve company logo
        logo_data = base64.b64decode(self.env.company.logo) if self.env.company.logo else None
        if logo_data:
            logo_stream = io.BytesIO(logo_data)
            worksheet.insert_image(0, 0, "logo.png", {'image_data': logo_stream, 'x_scale': 0.5, 'y_scale': 0.5})

        # Formatting
        title_format = workbook.add_format({'bold': True, 'font_size': 14})
        header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3'})
        total_format = workbook.add_format({'bold': True})

        # Section-1: Header
        worksheet.write(5, 0, "RFP Report", title_format)
        worksheet.write(6, 0, f"Supplier: {self.supplier_id.name}")
        worksheet.write(7, 0, f"Date Range: {self.start_date} - {self.end_date}")
        
        row = 9
        # Section-2: Table Headers
        headers = ['RFP Number', 'Date', 'Required Date', 'Total Amount']
        for col, header in enumerate(headers):
            worksheet.write(row, col, header, header_format)
        row += 1

        # Section-3: RFP Data
        for rfp in rfps:
            worksheet.write(row, 0, rfp.rfp_number)
            worksheet.write(row, 1, str(rfp.create_date))
            worksheet.write(row, 2, str(rfp.required_date))
            worksheet.write(row, 3, rfp.total_amount)
            row += 1

        row += 2
        # Section-4: Product Data Headers
        worksheet.write(row, 0, "Purchased Products", title_format)
        row += 1
        product_headers = ['Product Name', 'Quantity', 'Unit Price', 'Subtotal']
        for col, header in enumerate(product_headers):
            worksheet.write(row, col, header, header_format)
        row += 1

        for purchase in products:
            for line in purchase.order_line:
                worksheet.write(row, 0, line.product_id.name)
                worksheet.write(row, 1, line.product_qty)
                worksheet.write(row, 2, line.price_unit)
                worksheet.write(row, 3, line.price_subtotal)
                row += 1

        workbook.close()
        output.seek(0)

        # Convert file to base64
        file_data = base64.b64encode(output.getvalue())
        file_name = f"RFP_Report_{self.supplier_id.name}.xlsx"

        # Save file as attachment
        attachment = self.env['ir.attachment'].create({
            'name': file_name,
            'type': 'binary',
            'datas': file_data,
            'store_fname': file_name,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })

        # Store the file in the record
        self.report_file = file_data
        self.report_file_name = file_name

        # Return download action
        return {
            'type': 'ir.actions.act_url',
            'url': f"/web/content/{attachment.id}?download=true",
            'target': 'self',
        }