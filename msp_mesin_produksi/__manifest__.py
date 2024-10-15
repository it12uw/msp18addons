{
    'name': 'Mesin Produksi Marel',
    'summary': 'Mesin dan Kerusakan Marel',
    'version': '18.0',

    'description': """
Human readable name Module Project.
==============================================


    """,

    'author': 'asrent',
    # 'maintainer': 'TM_FULLNAME',
    # 'contributors': ['TM_FULLNAME <TM_FULLNAME@gmail.com>'],

    'website': 'asrent',

    'license': 'AGPL-3',
    'category': 'Uncategorized',

    'depends': [
        'base'
    ],
    # 'external_dependencies': {
    #     'python': [
    #     ],
    # },
    'data': [
        'security/ir.model.access.csv',
        'views/msp_mesin_produksi.xml',
        'views/jenis_kerusakan_mesin_marel.xml',
        'views/nama_teknisi.xml',
        'views/kerusakan_mesin_list.xml',
        'views/menu.xml',
        "views/merk_type_mesin.xml",
        "views/type_mesin_produksi.xml",
    ],
    'demo': [
    ],
    # 'js': [
    # ],
    # 'css': [
    # ],
    # 'qweb': [
    # ],
    # 'images': [
    # ],
    # 'test': [
    # ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
