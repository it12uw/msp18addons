{
    'name': 'Import Shopee To Sale Order',
    'version': '18.0',
    'category': 'Sales',
    'summary': 'Import and export CSV for sale module with extended fields',
    'description': """
        This module allows to import and export CSV files for the sale module with extended fields.
        It handles existing data and creates new records only when necessary.
    """,
    'author': 'Laksamana Morison',
    'website': 'https://stevencodelab.github.io/',
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_import_views.xml',
        'views/inherit_sale_order.xml',
        'wizard/sale_import_wizard.xml',
        'wizard/sale_export_wizard.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
