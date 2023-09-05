{
    'name' : 'Birthday Reminder',
    'version': '16.0.1',
    'description': 'Send the birthday wish mail automatically to the customer',
    'summary': '''It should send mail automatically if the customer have the birthday today.
                Its cron method run on every 00:00:00''',
    'category': 'tools',
    "license": "LGPL-3",
    'author': "Akili Systems Private Limited",
    'company': "Akili Systems Private Limited",
    'website': "http://www.akilisystems.in",
    'depends': ['base', 'mail','contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/dob_field_updation.xml',
        'views/email_template.xml',
        'views/customer_birthday_reminder.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
