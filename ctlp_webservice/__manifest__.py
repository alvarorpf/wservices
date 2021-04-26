# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2020 Poiesis Consulting S.R.L. (<https://www.poiesisconsulting.com>).
#    Autor: Alvaro Paredes Flores
#
##############################################################################
{
    'name': 'Servicios Web TodoTix',
    'version': '13.0',
    'category': 'Client',
    'summary': 'Adecuaciones Cliente',
    'description': """
* Servicios web para consultas y pagos mediante la plataforma de TodoTix

    """,
    'author': 'Poiesis Consulting',
    'website': 'http://www.poiesisconsulting.com',
    'depends': [
        'ctlp_collection',
    ],
    'external_dependencies': {

    },
    'data': [
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
}