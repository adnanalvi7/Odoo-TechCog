# # -*- coding: utf-8 -*-
# {
#     'name': "zkteco_remote_attendance",

#     'summary': "Short (1 phrase/line) summary of the module's purpose",

#     'description': """
# Long description of module's purpose
#     """,

#     'author': "My Company",
#     'website': "https://www.yourcompany.com",

#     # Categories can be used to filter modules in modules listing
#     # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
#     # for the full list
#     'category': 'Uncategorized',
#     'version': '0.1',

#     # any module necessary for this one to work correctly
#     'depends': ['base'],

#     # always loaded
#     'data': [
#         # 'security/ir.model.access.csv',
#         'views/views.xml',
#         'views/templates.xml',
#     ],
#     # only loaded in demonstration mode
#     'demo': [
#         'demo/demo.xml',
#     ],
# }

{
    'name': "ZKTeco Remote Attendance",
    'summary': "Allow employees to mark attendance remotely based on location coordinates",
    'author': "Fazeel Malik",
    'website': "https://www.yourwebsite.com",
    'category': 'Human Resources',
    'version': '1.0',
    'depends': ['web','hr_attendance', 'portal', 'hr'],
    'license': 'LGPL-3',
    'data': [
        'views/employee_view.xml',
        'security/ir.model.access.csv',
        'views/assets.xml'
    ],
    'assets': {
        'web.assets_frontend': [
            'zkteco_remote_attendance/static/src/js/portal_attendance.js',
        ],
    },
    'installable': True,
    
}


