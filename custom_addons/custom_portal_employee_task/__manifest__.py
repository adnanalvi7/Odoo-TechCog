{
    'name': 'Custom Portal Employee Task',
    'version': '1.0',
    'category': 'Project',
    'summary': 'Allow portal users to be assigned as employees and receive login credentials',
    'author': 'Fazeel Malik',
    'depends': ['base','hr_contract','project', 'hr', 'portal' ],
    'license': 'LGPL-3',
    'data': [
        'security/ir_model_access.xml',
        'views/employee_view.xml',
        'views/project_task_view.xml',
        
    ],
    'installable': True,
}
