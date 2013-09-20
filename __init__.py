# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution #    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).  # 
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
import helper
import pay_type
import points_config
import member_class                 #会员卡等级设置
import member                       #会员信息设置
import member_class_change_config   #会员升降级设置
import member_recharge_pref         #会员充值优惠
import member_charge                #会员充值
import member_consumption           #会员消费
import discount_card_type           #打折卡类别
import discount_card                #打折卡
import report
import wizard

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
