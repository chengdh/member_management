# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
    'name': 'member management',
    'version': '0.1',
    'category': 'member',
    "sequence": 0,
    'description': """
    会员管理
===================================================

主要功能 :
---------------
    * 会员等级
    * 会员设置
    * 打折卡
    """,
    'author': '程东辉',
    'images': [],
    'depends': ["base", "process", "decimal_precision"],
    'init_xml': [],
    'data' : [
#NOTE 要注意xml文件的顺序
        'security/ktv_security.xml',
        'views/base.xml',
        #'security/ir.model.access.csv',
        'views/points_config.xml',
        'views/member_class.xml',
        'views/member_class_change_config.xml',
        'views/member_recharge_pref.xml',
        'views/member.xml',
        'views/member_charge.xml',
        'views/discount_card_type.xml',
        ],
    'demo': [],
    'test': [],
    'installable': True,
    'application': True,
    # Web client
    'js': [],
    'css': [],
    'qweb': [],

}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
