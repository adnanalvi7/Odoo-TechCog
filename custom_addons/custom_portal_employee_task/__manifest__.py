{
    'name': 'Custom Portal Employee Task',
    'version': '1.0',
    'category': 'Project',
    'summary': 'Allow portal users to be assigned as employees and receive login credentials',
    'author': 'Fazeel Malik',
    'depends': ['hr_contract','project', 'hr', 'portal' ],
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/employee_view.xml',
        'views/project_task_view.xml',
        
    ],
    'installable': True,
}
