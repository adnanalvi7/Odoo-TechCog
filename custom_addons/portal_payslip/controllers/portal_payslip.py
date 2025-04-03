from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
import logging
import io
import xlsxwriter

_logger = logging.getLogger(__name__)

class CustomPortalPayslips(CustomerPortal):

    @http.route(['/my/payslips'], type='http', auth="user", website=True)
    def portal_my_payslips(self, **kw):
        """Render the payslip list view for the portal user."""
        user = request.env.user
        payslips = request.env['hr.payslip'].sudo().search([('employee_id.user_id', '=', user.id)])
            # Get employee's leave balance
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', user.id)], limit=1)
        pending_leaves = employee.allocation_remaining_display if employee else '0'
 
        values = {
            'payslips': payslips,
            'pending_leaves': pending_leaves
        }

        return request.render("portal_payslip.portal_payslips_page", values)

    
    @http.route(['/my/payslip/download/<int:payslip_id>'], type='http', auth="user", website=True)
    def download_payslip(self, payslip_id, **kwargs):
        """Try to download the payslip as PDF, fallback to Excel if PDF fails."""
        payslip = request.env['hr.payslip'].sudo().browse(payslip_id)
        

        if not payslip or payslip.employee_id.user_id != request.env.user:
            return request.redirect('/my/payslips')

        # Fetch the correct report object
        report = request.env.ref('hr_payroll.report_payslip_lang')
        if not report:
            _logger.error("Payslip Report not found: hr_payroll.report_payslip_lang")
            return self.generate_excel(payslip)  # Fallback to Excel

        try:
            # Generate PDF report
            pdf_content, content_type = report.sudo()._render_qweb_pdf([payslip.id])

            if not pdf_content:
                _logger.error("Failed to generate PDF for Payslip ID %s", payslip.id)
                return self.generate_excel(payslip)  # Fallback to Excel

            pdf_filename = f"Payslip_{payslip.number or payslip.id}.pdf"

            return request.make_response(
                pdf_content,
                headers=[
                    ('Content-Type', 'application/pdf'),
                    ('Content-Disposition', f'attachment; filename="{pdf_filename}"')
                ]
            )
        except Exception as e:
            _logger.exception("Error generating payslip PDF: %s", str(e))
            return self.generate_excel(payslip)  # Fallback to Excel

    def generate_excel(self, payslip):
        """Generate and download an Excel file with proper column width and status."""
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet('Payslip')

        bold = workbook.add_format({'bold': True})

        # Define headers
        headers = ['Employee', 'Payslip Reference', 'Date From', 'Date To', 'Total Amount', 'Status' , 'Leave Balance']
        column_widths = [len(header) for header in headers]  # Initialize column width based on header length

        # Write headers
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, bold)

        # Payslip Data
        payslip_data = [
            payslip.employee_id.name,
            payslip.number or 'N/A',
            str(payslip.date_from),
            str(payslip.date_to),
            payslip.line_ids and payslip.line_ids[0].total or 0.0,
            payslip.state,  # Adding status
            payslip.employee_id.allocation_remaining_display or 0
        ]

        for col, value in enumerate(payslip_data):
            worksheet.write(1, col, value)
            column_widths[col] = max(column_widths[col], len(str(value)))  # Adjust column width based on data

         # Auto-adjust column width
        for col, width in enumerate(column_widths):
            worksheet.set_column(col, col, width + 2)  # Add padding for better visibility

        workbook.close()
        output.seek(0)

        excel_filename = f"Payslip_{payslip.number or payslip.id}.xlsx"

        return request.make_response(
            output.read(),
            headers=[
            ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
            ('Content-Disposition', f'attachment; filename="{excel_filename}"')
            ]
    )