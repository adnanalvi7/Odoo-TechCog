# -*- coding: utf-8 -*-
# from odoo import http


# class ZktecoAttendance(http.Controller):
#     @http.route('/zkteco_attendance/zkteco_attendance', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/zkteco_attendance/zkteco_attendance/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('zkteco_attendance.listing', {
#             'root': '/zkteco_attendance/zkteco_attendance',
#             'objects': http.request.env['zkteco_attendance.zkteco_attendance'].search([]),
#         })

#     @http.route('/zkteco_attendance/zkteco_attendance/objects/<model("zkteco_attendance.zkteco_attendance"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('zkteco_attendance.object', {
#             'object': obj
#         })

# controllers.py
from odoo import http
from odoo.http import request
import json

class BiometricAttendanceController(http.Controller):
    @http.route('/biometric/attendance', type='json', auth='public', methods=['POST'], csrf=False)
    def receive_attendance(self, **post):
        """ Receive attendance from the intermediary server. """
        data = request.jsonrequest
        employee_id = data.get("employee_id")
        timestamp = data.get("timestamp")
        status = data.get("status")

        # Find the employee in Odoo by the device's employee ID
        employee = request.env['hr.employee'].sudo().search([('biometric_employee_id', '=', employee_id)], limit=1)
        
        if employee:
            # Check for existing attendance and avoid duplicates
            existing_attendance = request.env['hr.attendance'].sudo().search([
                ('employee_id', '=', employee.id),
                ('check_in', '<=', timestamp),
                ('check_out', '>=', timestamp),
            ], limit=1)

            if existing_attendance:
                return {"status": "success", "message": "Attendance already recorded"}

            # Record the attendance (check-in or check-out)
            if status == 'in':
                request.env['hr.attendance'].sudo().create({
                    'employee_id': employee.id,
                    'check_in': timestamp
                })
            elif status == 'out':
                last_attendance = request.env['hr.attendance'].sudo().search([
                    ('employee_id', '=', employee.id),
                    ('check_out', '=', False)
                ], order="check_in desc", limit=1)

                if last_attendance:
                    last_attendance.write({'check_out': timestamp})
                else:
                    return {"status": "error", "message": "No previous check-in found for check-out"}

            return {"status": "success", "message": "Attendance recorded successfully"}
        else:
            return {"status": "error", "message": "Employee not found"}
