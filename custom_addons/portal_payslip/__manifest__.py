{
    'name': 'Portal Payslip',
    'summary': 'Allow portal users to view their payslips',
    'version': '1.0',
    'depends': ['base','portal', 'hr_payroll', 'hr_contract', 'hr_holidays' , 'web' , 'hr_timesheet' , 'l10n_us_hr_payroll' , 'sale_timesheet'],
    'license': 'LGPL-3',
    'data': [
        'views/portal_payslip_templates.xml',
        'views/portal_payslip_page.xml',
        'views/views.xml',
        'views/assets.xml'
    ],
   'assets': {
    'web.assets_frontend': [
        'portal_payslip/static/src/css/style.css',
    ],
    },

    'installable': True,
}
