# from odoo import models, fields, api

# class Employee(models.Model):
#     _inherit = 'hr.employee'

#     def create_user_for_employee(self):
#         if not self.user_id and self.work_email:
#             portal_group = self.env.ref('base.group_portal')
            
#             # Get other user-type groups that may conflict
#             conflicting_groups = self.env['res.groups'].search([
#                 ('id', '!=', portal_group.id),
#                 ('category_id.name', '=', 'User types')
#             ])

#             # Create the user
#             user = self.env['res.users'].create({
#                 'name': self.name,
#                 'login': self.work_email,
#                 'groups_id': [(6, 0, [self.env.ref('base.group_portal').id])],  # Assign Portal Access
#                 'share': True,  # Mark as portal user
#                 'image_1920': self.image_1920,  # Copy Employee Image to User
#             })

#             # Remove any conflicting groups just in case
#             user.groups_id -= conflicting_groups
#             # Assign user to employee
#             self.user_id = user

#             # 🔹 Force work_email to persist (Fixes disappearing email issue)
#             self.work_email = user.login

#             # 🔹 Link employee to the same partner as user (Prevents duplicate contacts)
#             if user.partner_id and not self.address_id:
#                 self.address_id = user.partner_id  

#     # @api.model
#     # def create(self, vals):
#     #     """ Override create method to create a portal user and prevent duplicate contacts """
        
#     #     # 🔹 Ensure work email is assigned before saving
#     #     # if not vals.get('work_email'):
#     #     #     raise ValueError("Work Email is required to create a user.")
#     #         # 🔹 Skip email validation in test mode to prevent Odoo test failures
#     #     if not self.env.context.get('test_mode') and not self.env.context.get('install_mode') and not vals.get('work_email'):
#     #         raise ValueError("Work Email is required to create a user.")

#     #     employee = super(Employee, self).create(vals)

#     #     # 🔹 Create the user only if not already assigned
#     #     if not employee.user_id:
#     #         employee.create_user_for_employee()

#     #     # 🔹 Ensure employee and user share the same contact (Prevents duplicate contacts)
#     #     if employee.user_id and not employee.address_id:
#     #         employee.address_id = employee.user_id.partner_id  

#     #     return employee
#     @api.model_create_multi
#     def create(self, vals_list):
#         """ Override create method to create a portal user and prevent duplicate contacts """
        
#         for vals in vals_list:
#             if not self.env.context.get('test_mode') and not self.env.context.get('install_mode') and not vals.get('work_email'):
#                 raise ValueError("Work Email is required to create a user.")

#         employees = super(Employee, self).create(vals_list)

#         for employee in employees:
#             # 🔹 Create the user only if not already assigned
#             if not employee.user_id:
#                 employee.create_user_for_employee()

#             # 🔹 Ensure employee and user share the same contact (Prevents duplicate contacts)
#             if employee.user_id and not employee.address_id:
#                 employee.address_id = employee.user_id.partner_id  

#         return employees


#     def write(self, vals):
#         """ Sync profile picture with user when updated """
#         res = super(Employee, self).write(vals)

#         if 'image_1920' in vals and self.user_id:
#             self.user_id.sudo().write({'image_1920': vals['image_1920']})  # Update user image when employee image changes

#         return res


# from odoo import models, fields, api

# class Employee(models.Model):
#     _inherit = 'hr.employee'

#     def create_user_for_employee(self):
#         """ Create a portal user for the employee if not already assigned """
#         if not self.user_id and self.work_email:

#             # Only block if demo/install data via XML (not manual UI/API)
#             if self.env.context.get('install_mode') or self.env.context.get('xml_id'):
#                 return

#             portal_group = self.env.ref('base.group_portal')
#             user_type_groups = self.env['res.groups'].search([
#                 ('category_id.name', '=', 'User types'),
#                 ('id', '!=', portal_group.id)
#             ])

#             user = self.env['res.users'].create({
#                 'name': self.name,
#                 'login': self.work_email,
#                 'groups_id': [(6, 0, [portal_group.id])],
#                 'share': True,
#                 'image_1920': self.image_1920,
#             })

#             # Clean up conflicting groups just in case
#             user.groups_id -= user_type_groups

#             self.user_id = user
#             self.work_email = user.login

#             if user.partner_id and not self.address_id:
#                 self.address_id = user.partner_id

#     @api.model_create_multi
#     def create(self, vals_list):
#         employees = super(Employee, self).create(vals_list)

#         for employee in employees:
#             # Allow only outside of install/demo XML data
#             if not self.env.context.get('install_mode') and not self.env.context.get('xml_id'):
#                 if not employee.user_id:
#                     employee.create_user_for_employee()

#                 if employee.user_id and not employee.address_id:
#                     employee.address_id = employee.user_id.partner_id

#         return employees

#     def write(self, vals):
#         res = super(Employee, self).write(vals)

#         if 'image_1920' in vals and self.user_id:
#             self.user_id.sudo().write({'image_1920': vals['image_1920']})

#         return res


from odoo import models, fields, api

class Employee(models.Model):
    _inherit = 'hr.employee'

    def create_user_for_employee(self):
        """ Create a portal user for the employee if not already assigned """
        if not self.user_id and self.work_email:

            # Block only during test/demo loads — not during regular creation
            if self.env.context.get('demo') or self.env.context.get('test_mode'):
                return

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

            # Remove conflicting user type groups
            user.groups_id -= user_type_groups

            self.user_id = user
            self.work_email = user.login

            if user.partner_id and not self.address_id:
                self.address_id = user.partner_id

    @api.model_create_multi
    def create(self, vals_list):
        employees = super(Employee, self).create(vals_list)

        for employee in employees:
            # Allow creation unless it's during test/demo mode
            if not self.env.context.get('demo') and not self.env.context.get('test_mode'):
                if not employee.user_id:
                    employee.create_user_for_employee()

                if employee.user_id and not employee.address_id:
                    employee.address_id = employee.user_id.partner_id

        return employees

    def write(self, vals):
        res = super(Employee, self).write(vals)

        if 'image_1920' in vals and self.user_id:
            self.user_id.sudo().write({'image_1920': vals['image_1920']})

        return res
