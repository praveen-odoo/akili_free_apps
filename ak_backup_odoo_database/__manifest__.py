# -*- coding: utf-8 -*-
{
    'name': "ak_backup_odoo_database",

    'summary': """It back up the database at a given period and time.""",

    'description': """
        It back up the database at a given period and time and stores it at the user's given location.
        User can download the backup of database from stored location.
    """,

    'author': "Akili systems Pvt. Ltd.",
    'website': "http://www.akilisystems.in",
    'category': 'Database',
    'version': '15.0',
    "license": "LGPL-3",

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/database_backup_view.xml',
    ],
    
}
