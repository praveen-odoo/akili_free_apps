# Copyright 2018 Akili Systems Pvt. Ltd. India

{
    'name' : 'SO/Invoice Reports with Product Image',
    "summary": "Show product images on Sale Order Line as well on sale/invoice reports",
    "version": "15.0.1.0.0",
    'category': 'Sales',
    "website": "https://akilisystems.in",
    'author': "Akili Systems Pvt. Ltd.",
    'company': "Akili Systems Pvt. Ltd.",
    "license": "AGPL-3",
    'depends': ['base','sale_management', 'account','sale'],
    'data': [
        'views/sale_order_line_image.xml',
        'views/invoice_move_line_image.xml',
        'report/sale_report.xml',
        'report/invoice_report.xml'
    ],
    'images': ['static/description/banner.jpg'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
