# -*- coding: utf-8 -*-
#会员充值优惠设置信息
from osv import fields, osv
import decimal_precision as dp

class member_recharge_pref(osv.osv):
  '''
  会员充值优惠设置
  '''
  _name = "member_management.member_recharge_pref"
  _description = "会员充值优惠"

  _columns = {
      "name" : fields.char("name",size = 60,select = True,help="名称",required = True),
      "member_class_id" : fields.many2one("member_management.member_class","member_class_id",select = True,required = True,help = "会员等级"),
      "start_fee" : fields.float("start_fee", digits_compute= dp.get_precision('member_management_fee'),help ="起始金额"),
      "end_fee" : fields.float("end_fee", digits_compute= dp.get_precision('member_management_fee'),help ="结束金额"),
      "pref_fee" : fields.float("pref_fee", digits_compute= dp.get_precision('member_management_fee'),help ="优惠金额"),
      "active" : fields.boolean("active"),
      }

  _defaults = {
      'active' : True,
      'start_fee' : 0,
      'end_fee' :   0,
      'pref_fee' :  0,
      }
