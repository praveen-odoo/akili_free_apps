# Copyright 2018 Akili Systems Pvt. Ltd. India
{
    'name': "Employee Document Management",

    'summary': """
        With the help of this module you can manage the documents of your employee.""",

    'description': """
        With the help of this module you can manage the documents of your employee and send the mail of expiration 
        of the document.
    """,

    'author': "Akili systems Pvt. Ltd.",
    'website': "http://www.akilisystems.in",
    'category': "tools",
    'version': "16.0.1",
    "license": "LGPL-3",

    # any module necessary for this one to work correctly
    'depends': ['hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/employee_documents_management.xml',
        'views/employee_documents_reminder.xml',
        'views/email_template.xml'
    ],
    'images': ['static/description/banner.jpg'],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'autoinstall': False,
    'installable': True,
    'application': False
}
