# -*- coding: utf-8 -*-
#会员充值
from osv import fields, osv
import helper
import decimal_precision as dp
from pay_type import pay_type

class member_charge(osv.osv):
    '''会员充值信息'''
    _name = "member_management.member_charge"
    _descripton = "会员充值设置"

    _columns = {
        "member_id" : fields.many2one("member_management.member","member_id",select = True,required = True,help="会员卡号"),
        "bill_datetime" : fields.datetime('bill_date',required = True,help = "充值时间"),
        "charge_fee" : fields.float("charge_fee",digits_compute = dp.get_precision('member_management_fee'),help = "本次充值金额"),
        "before_charge_balance" : fields.float("before_charge_banalce",readonly = True,digits_compute = dp.get_precision('member_management_fee'),help = "充值前卡余额"),
        "after_charge_balance" : fields.float("after_charge_banalce",readonly = True,digits_compute = dp.get_precision('member_management_fee'),help = "充值后卡余额"),
        "charge_points" : fields.integer("charge_points",help = "本次充值积分"),
        "before_charge_points" : fields.integer("before_charge_points",help="充值前卡积分"),
        "after_charge_points" : fields.integer('after_charge_points',help="充值后卡积分"),
        "pay_type_id" : fields.many2one('member_management.pay_type','pay_type_id',required = True,help="付款方式"),
        "present_charge_fee" : fields.float("present_charge_fee",readonly = True,digits_compute = dp.get_precision('member_management_fee'),help="本次赠送金额"),
        "printed" : fields.boolean("printed",readonly = True,help="是否已打印"),
        "active" : fields.boolean("active"),
        }

    _defaults = {
        "bill_datetime" : fields.datetime.now,
        "charge_fee" : 0.0,
        "before_charge_balance" : 0.0,
        "after_charge_balance" : 0.0,
        "charge_points" : 0,
        "before_charge_points" : 0,
        "after_charge_points" : 0,
        "present_charge_fee" : 0.0,
        "pay_type_id" : lambda obj,cr,uid,context :  obj.pool.get('member_management.pay_type').get_pay_type_id(cr,uid,pay_type.PAY_TYPE_CASH),
        "printed" : False,
        "active" : True,
        }

    def onchange_member_id_or_charge_fee(self,cr,uid,ids,member_id,charge_fee):
      '''
      member_id发生变化时,需要处理赠送金额
      '''
      if not member_id :
        return {}

      present_fee = 0.0
      pool = self.pool
      member = pool.get('member_management.member').browse(cr,uid,member_id)
      #获取会员充值优惠设置
      if charge_fee > 0:
        member_class_id = member.member_class_id.id
        pref_ids = pool.get('member_management.member_recharge_pref').search(cr,uid,[('member_class_id','=',member_class_id)])
        active_prefs = [pref for pref in pool.get('member_management.member_recharge_pref').browse(cr,uid,pref_ids) if charge_fee >= pref.start_fee and charge_fee <= pref.end_fee]
        if active_prefs:
          present_fee = active_prefs[0].pref_fee

      vals = {
        'present_charge_fee'    : present_fee,
        'before_charge_balance' : member.balance,
        'after_charge_balance'  : member.balance + charge_fee + present_fee,
        }

      return {"value" : vals}

    def print_info(self,cr,uid,id,context):
      '''
      获取打印信息
      '''
      #判断是否已打印

      vals = self.read(cr,uid,id,context)
      if not vals['printed']:
        self.write(cr,uid,id,{'printed' : True})

      member = self.pool.get('member_management.member').read(cr,uid,vals['member_id'][0])
      vals['member_id'] = member
      return vals
