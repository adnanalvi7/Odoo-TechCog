from odoo import models, fields, api

class Employee(models.Model):
    _inherit = 'hr.employee'

    def create_user_for_employee(self):
        """Create a portal user for the employee if not already assigned"""

        # ⚠️ Skip during install, demo or test mode
        if self.env.context.get('install_mode') or self.env.context.get('demo') or self.env.context.get('test_mode'):
            return

        if not self.user_id and self.work_email:
            portal_group = self.env.ref('base.group_portal')
            user_type_groups = self.env['res.groups'].search([
                ('category_id.name', '=', 'User types'),
                ('id', '!=', portal_group.id)
            ])

            user = self.env['res.users'].create({
                'name': self.name,
                'login': self.work_email,
                'groups_id': [(6, 0, [portal_group.id])],
                'share': True,
                'image_1920': self.image_1920,
            })

            # Remove conflicting user types
            user.groups_id -= user_type_groups

            self.user_id = user
            self.work_email = user.login

            if user.partner_id and not self.address_id:
                self.address_id = user.partner_id

    @api.model_create_multi
    def create(self, vals_list):
        employees = super().create(vals_list)

        for employee in employees:
            employee.create_user_for_employee()

        return employees

    def write(self, vals):
        res = super().write(vals)

        if 'image_1920' in vals:
            for emp in self:
                if emp.user_id:
                    emp.user_id.sudo().write({'image_1920': vals['image_1920']})

        return res

