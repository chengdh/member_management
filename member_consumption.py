# -*- coding: utf-8 -*-
#会员卡结账信息
from osv import fields, osv
import helper
import decimal_precision as dp

class member_consumption(osv.osv):
    '''会员卡结账信息'''
    _name = "member_management.member_consumption"
    _descripton = "会员卡结账信息(包括超市结账和ktv结账)"

    _columns = {
        "member_id" : fields.many2one("member_management.member","member_id",select = True,required = True,help="会员卡号"),
        "bill_datetime" : fields.datetime("bill_datetime",required = True,help = "结账时间"),
        #"room_operate_id" : fields.many2one('ktv.room_operate','room_operate',help="本次结账关联的room_operate"),
        #"order_id" : fields.many2one('pos.order','order_id',help="本次结账关联的超市账单"),
        "total_paid_fee" : fields.float("total_paid_fee",digits_compute = dp.get_precision('member_management_fee'),help = "本次付款金额合计,该字段用于积分"),
        "paid_fee" : fields.float("paid_fee",digits_compute = dp.get_precision('member_management_fee'),help = "本次使用会员卡付款金额"),
        "before_paid_balance" : fields.float("before_paid_banalce",readonly = True,digits_compute = dp.get_precision('member_management_fee'),help = "付款前卡余额"),
        "after_paid_balance" : fields.float("after_paid_banalce",readonly = True,digits_compute = dp.get_precision('member_management_fee'),help = "付款后卡余额"),
        "points" : fields.integer("points",help = "本次消费积分"),
        "before_paid_points" : fields.integer("before_paid_points",help="消费前卡积分"),
        "after_paid_points" : fields.integer('after_paid_points',help="消费后卡积分"),
        "active" : fields.boolean("active"),
        }

    _defaults = {
        "bill_datetime" : fields.datetime.now,
        "paid_fee" : 0.0,
        "total_paid_fee" : 0.0,
        "before_paid_balance" : 0.0,
        "after_paid_balance" : 0.0,
        "points" : 0,
        "before_paid_points" : 0,
        "after_paid_points" : 0,
        "active" : True,
        }

    def create(self,cr,uid,vals,context={}):
      '''
      重写create,根据积分设置规则计算会员积分
      '''
      pool = self.pool
      member = pool.get('member_management.member').browse(cr,uid,vals['member_id'])
      #计算会员卡积分设置
      the_points = pool.get('member_management.points_config').calculate_room_fee_points(cr,uid,vals['total_paid_fee'])
      vals.update({
        'before_paid_balance' : member.balance ,
        'after_paid_balance'  : member.balance - vals['paid_fee'],
        'before_paid_points'  : member.points, 
        'after_paid_points'   : member.points + the_points,
        'points'              : the_points,
        })

      return super(member_consumption,self).create(cr,uid,vals,context)

