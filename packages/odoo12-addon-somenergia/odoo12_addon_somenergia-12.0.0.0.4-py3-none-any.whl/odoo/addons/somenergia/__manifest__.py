{
    'name': "Odoo Som Energia customizations",
    'version': '12.0.0.0.4',
    'depends': [
        'account_asset_management',
        'account_invoice_import',
        'account_invoice_import_facturae',
        'hr_attendance_report_theoretical_time',
        'hr_expense',
        'contacts',
    ],
    'author': "Coopdevs Treball SCCL",
    'website': 'https://coopdevs.org',
    'category': "Cooperative management",
    'description': """ 
    Odoo Som Energia customizations.
    """,
    "license": "AGPL-3",
    'demo': [
        'demo/hr_leave_demo.xml',
    ],
    'data': [
        'views/hidden_menus.xml',
        'views/account_asset_profile.xml',
        'data/resource_data.xml',
        'data/leave_type.xml',
        'data/hr_leave_data.xml',
        'views/hr_attendance_view.xml',
        'views/hr_attendance_theoretical_time_report.xml',
        'views/hr_leave_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}

