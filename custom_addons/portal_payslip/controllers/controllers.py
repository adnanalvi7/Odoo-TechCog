# from odoo import http
# from odoo.http import request
# from odoo.addons.portal.controllers.portal import CustomerPortal

# class CustomPortalPayslips(CustomerPortal):

#     def _prepare_home_portal_values(self, counters):
#         values = super()._prepare_home_portal_values(counters)
#         user = request.env.user
#         payslip_model = request.env['hr.payslip']
        
#         # Fetch payslips for the current user
#         payslips = payslip_model.sudo().search([('employee_id.user_id', '=', user.id)])
        
#         values['payslips'] = payslips
#         return values
