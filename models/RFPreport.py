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
        print("rfps", rfps)
        return self.env.ref('supplier_management.rfp_report_html_preview_action').report_action(self, data={'rfps': rfps.ids})


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

        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('RFP Report')

        # Formats
        title_format = workbook.add_format({'bold': True, 'font_size': 14})
        header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3'})
        total_format = workbook.add_format({'bold': True})

        # Section-1: Company Logo and Supplier Info
        logo_data = b64decode(self.env.company.logo)
        image = Image.open(io.BytesIO(logo_data))
        image_stream = io.BytesIO()
        image.save(image_stream, format='PNG')
        worksheet.insert_image('A1', 'company_logo.png', {'image_data': image_stream.getvalue(), 'x_scale': 0.5, 'y_scale': 0.5})

        row = 0
        col = 3
        worksheet.write(row, col, self.supplier_id.name, title_format)
        row += 2

        supplier_info = [
            ('Email:', self.supplier_id.email or ''),
            ('Phone:', self.supplier_id.phone or ''),
            ('Address:', f"{self.supplier_id.street or ''}, {self.supplier_id.city or ''}, {self.supplier_id.country_id.name or ''}"),
            ('TIN:', self.supplier_id.vat or ''),
            ('Bank Name:', self.supplier_id.bank_ids[0].bank_name if self.supplier_id.bank_ids else ''),
            ('Account Name:', self.supplier_id.bank_ids[0].acc_holder_name if self.supplier_id.bank_ids else ''),
            ('Account Number:', self.supplier_id.bank_ids[0].acc_number if self.supplier_id.bank_ids else ''),
            ('IBAN:', self.supplier_id.bank_ids[0].iban if self.supplier_id.bank_ids else ''),
            ('SWIFT:', self.supplier_id.bank_ids[0].bic if self.supplier_id.bank_ids else '')
        ]
        for label, value in supplier_info:
            if value:
                worksheet.write(row, col, label)
                worksheet.write(row, col + 1, value)
                row += 1

        # Section-2: RFPs Table
        row += 2
        headers = ['RFP Number', 'Date', 'Required Date', 'Total Amount']
        for idx, header in enumerate(headers):
            worksheet.write(row, idx, header, header_format)
        row += 1

        rfp_total = 0
        for rfp in rfps:
            worksheet.write(row, 0, rfp.rfp_number)
            worksheet.write(row, 1, rfp.create_date.strftime('%d/%m/%Y'))
            worksheet.write(row, 2, rfp.required_date.strftime('%d/%m/%Y'))
            worksheet.write(row, 3, rfp.total_amount)
            rfp_total += rfp.total_amount
            row += 1

        worksheet.write(row, 2, 'Total', total_format)
        worksheet.write(row, 3, rfp_total, total_format)

        # Section-3: Product Lines Table
        row += 2
        headers = ['Product Name', 'Quantity', 'Unit Price', 'Delivery Charges', 'Subtotal Price']
        for idx, header in enumerate(headers):
            worksheet.write(row, idx, header, header_format)
        row += 1

        product_totals = {}
        for rfp in rfps:
            for line in rfp.product_line_ids:
                product = line.product_id
                if product not in product_totals:
                    product_totals[product] = {'qty': 0, 'unit_price': 0, 'delivery_charges': 0, 'subtotal': 0}
                product_totals[product]['qty'] += line.quantity
                product_totals[product]['unit_price'] = line.unit_price
                product_totals[product]['delivery_charges'] += line.delivery_charges or 0
                product_totals[product]['subtotal'] += line.subtotal_price

        product_total = 0
        for product, totals in product_totals.items():
            worksheet.write(row, 0, product.name)
            worksheet.write(row, 1, totals['qty'])
            worksheet.write(row, 2, totals['unit_price'])
            worksheet.write(row, 3, totals['delivery_charges'])
            worksheet.write(row, 4, totals['subtotal'])
            product_total += totals['subtotal']
            row += 1

        worksheet.write(row, 3, 'Total', total_format)
        worksheet.write(row, 4, product_total, total_format)

        # Section-4: Company Info
        row += 2
        company_info = [
            f"Email: {self.env.company.email or ''}",
            f"Phone: {self.env.company.phone or ''}",
            f"Address: {self.env.company.street or ''}, {self.env.company.city or ''}, {self.env.company.country_id.name or ''}"
        ]
        for info in company_info:
            worksheet.write(row, 0, info)
            row += 1

        workbook.close()
        output.seek(0)

        # Save the file in the attachment for download
        attachment = self.env['ir.attachment'].create({
            'name': 'RFP_Report.xlsx',
            'type': 'binary',
            'datas': base64.b64encode(output.getvalue()),
            'store_fname': 'RFP_Report.xlsx',
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }