# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016  Goran Sunjka  (http://www.sunjka.de)
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Partner Project Expertise',
    'version': '9.0.1.0.0',
    'category': 'Projects & Services',
    'sequence': 14,
    'summary': '',
    'description': """
Partner Project Expertise
============
    Add expertise to partner and project.
    """,
    'author':  'Goran Sunjka',
    'website': 'www.sunjka.de',
    'license': 'AGPL-3',
    'images': [
    ],
    'depends': [
        'project',
    ],
    'data': [
        'security/ir.model.access.csv',
        'view/project_view.xml',
        'view/partner_view.xml',
        'view/expertise_view.xml',
    ],
    'demo': [
        'data/demo.xml',
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: