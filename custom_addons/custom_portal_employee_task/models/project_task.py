# from odoo import models, fields, api

# class ProjectTask(models.Model):
#     _inherit = "project.task"
#     employee_id = fields.Many2one('hr.employee', string="Assigned Employee")
#     @api.model
#     def _get_user_domain(self):
#         return "[('|', ('share', '=', True), ('groups_id', 'in', [ref('base.group_user')]))]"

#     user_id = fields.Many2one(
#         'res.users', 
#         string='Assigned To', 
#         domain=_get_user_domain,  
#         help="Assign this task to an internal user or a portal user."
#     )



# from odoo import models, fields, api

# class ProjectTask(models.Model):
#     _inherit = "project.task"

#     @api.model
#     def _get_user_domain(self):
#         """Allow both internal users and portal users in the Assignees field"""
#         return "[('share', '=', False), ('groups_id', 'in', [ref('base.group_user')]), ('share', '=', True)]"

#     user_id = fields.Many2one(
#         'res.users',
#         string='Assigned To',
#         domain=_get_user_domain,
#         help="Assign this task to an internal user or a portal user."
#     )


from odoo import models, fields, api

class ProjectTask(models.Model):
    _inherit = "project.task"

    def _get_user_domain(self):
        """ Override domain to include portal users and internal users """
        return "[('share', 'in', [True, False])]"  # Allow both portal & internal users

    user_ids = fields.Many2many(
        'res.users',
        string="Assignees",
        domain=_get_user_domain,  
        help="Assign this task to an internal user or a portal user."
    )

    @api.model
    def get_users_to_assign(self):
        """ Override the default method that filters only internal users """
        return self.env['res.users'].search([('share', 'in', [True, False])])



