# from odoo import models, fields, api

# class Employee(models.Model):
#     _inherit = 'hr.employee'

#     def create_user_for_employee(self):
#         """ Create a portal user for the employee if not already assigned """
#         if not self.user_id:
#             if not self.work_email:
#                 raise ValueError("Please enter Work Email before saving.")  # Prevents empty emails

#             # Create the user
#             user = self.env['res.users'].create({
#                 'name': self.name,
#                 'login': self.work_email,
#                 'groups_id': [(6, 0, [self.env.ref('base.group_portal').id])],  # Assign Portal Access
#                 'share': True,  # Mark as portal user
#             })
            
#             # Assign user to employee
#             self.user_id = user

#             # 🔹 Force work_email to persist (Fixes disappearing email issue)
#             self.work_email = user.login

#             # 🔹 Link employee to the same partner as user (Prevents duplicate contacts)
#             if user.partner_id and not self.address_id:
#                 self.address_id = user.partner_id  # ✅ Use `address_home_id` instead of `partner_id`

#     @api.model
#     def create(self, vals):
#         """ Override create method to create a portal user and prevent duplicate contacts """
        
#         # 🔹 Ensure work email is assigned before saving
#         if 'work_email' in vals and not vals['work_email']:
#             raise ValueError("Work Email is required to create a user.")

#         employee = super(Employee, self).create(vals)

#         # 🔹 Create the user immediately (Fixes first save issue)
#         employee.create_user_for_employee()

#         # 🔹 Ensure employee and user share the same contact (Prevents duplicate contacts)
#         if employee.user_id and not employee.address_id:
#             employee.address_id = employee.user_id.partner_id  # ✅ Use `address_home_id`

#         return employee


from odoo import models, fields, api

class Employee(models.Model):
    _inherit = 'hr.employee'

    def create_user_for_employee(self):
        """ Create a portal user for the employee if not already assigned """
        if not self.user_id:
            if not self.work_email:
                raise ValueError("Please enter Work Email before saving.")  # Prevents empty emails

            # Create the user
            user = self.env['res.users'].create({
                'name': self.name,
                'login': self.work_email,
                'groups_id': [(6, 0, [self.env.ref('base.group_portal').id])],  # Assign Portal Access
                'share': True,  # Mark as portal user
                'image_1920': self.image_1920,  # Copy Employee Image to User
            })
            
            # Assign user to employee
            self.user_id = user

            # 🔹 Force work_email to persist (Fixes disappearing email issue)
            self.work_email = user.login

            # 🔹 Link employee to the same partner as user (Prevents duplicate contacts)
            if user.partner_id and not self.address_id:
                self.address_id = user.partner_id  

    @api.model
    def create(self, vals):
        """ Override create method to create a portal user and prevent duplicate contacts """
        
        # 🔹 Ensure work email is assigned before saving
        if 'work_email' in vals and not vals['work_email']:
            raise ValueError("Work Email is required to create a user.")

        employee = super(Employee, self).create(vals)

        # 🔹 Create the user immediately (Fixes first save issue)
        employee.create_user_for_employee()

        # 🔹 Ensure employee and user share the same contact (Prevents duplicate contacts)
        if employee.user_id and not employee.address_id:
            employee.address_id = employee.user_id.partner_id  

        return employee

    def write(self, vals):
        """ Sync profile picture with user when updated """
        res = super(Employee, self).write(vals)

        if 'image_1920' in vals and self.user_id:
            self.user_id.sudo().write({'image_1920': vals['image_1920']})  # Update user image when employee image changes

        return res
