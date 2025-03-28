# -*- coding: utf-8 -*-
# from odoo import http


# class CustomPortalEmployeeTask(http.Controller):
#     @http.route('/custom_portal_employee_task/custom_portal_employee_task', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_portal_employee_task/custom_portal_employee_task/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_portal_employee_task.listing', {
#             'root': '/custom_portal_employee_task/custom_portal_employee_task',
#             'objects': http.request.env['custom_portal_employee_task.custom_portal_employee_task'].search([]),
#         })

#     @http.route('/custom_portal_employee_task/custom_portal_employee_task/objects/<model("custom_portal_employee_task.custom_portal_employee_task"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_portal_employee_task.object', {
#             'object': obj
#         })

