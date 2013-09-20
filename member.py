# -*- coding: utf-8 -*-
#会员信息
from osv import fields, osv
import decimal_precision as dp
import helper

class member(osv.osv):
    '''会员信息设置'''
    _name = "member_management.member"
    _descripton = "会员信息"

    _rec_name = "member_no"

    def _compute_balance_and_points(self,cr,uid,ids,field_name,args,context):
      '''
      计算卡余额与积分
      '''
      ret = {}

      for record in  self.browse(cr,uid,ids):
        sum_charge = sum_present_charge_fee = sum_consumption = sum_balance =  0.0
        sum_points = 0
        for charge in record.member_charge_ids:
          sum_charge += charge.charge_fee                       #充值金额合计
          sum_present_charge_fee += charge.present_charge_fee   #充值赠送金额合计
        for consumption in record.member_consumption_ids:
          sum_consumption += consumption.paid_fee
          sum_points += consumption.points

        ret[record.id] = {
            'balance' : sum_charge + sum_present_charge_fee - sum_consumption,
            #TODO  计算积分点数时,需要减去积分兑换中扣除的积分
            'points' : sum_points,
            }

      return ret


    _columns ={
            "member_no" : fields.char("member_no",size = 30,readonly = True,select = True,help="会员编号,由系统自动生成",required = True),
            "name" : fields.char("name",size = 20,required = True,help = "会员名称"),
            "member_class_id" : fields.many2one("member_management.member_class","member_class_id",select = True,required = True,help = "会员等级"),
            "member_card_no" : fields.char("card_id",size = 30,select= True,required = True,help = "会员卡号,卡具上印刷的编号"),
            "photo" : fields.binary("photo",filter=".jpg,.png,.bmp"),
            "card_fee" : fields.float("make_fee",digits =  (10,2),help = "制卡费用,默认取会员等级中的制卡费用"),
            "up_card_fee" : fields.float("up_card_fee",digits =  (10,2),help = "补卡费用,默认取会员等级中的制卡费用"),
            "begin_datetime" : fields.datetime("begin_datetime",readonly = True,required = True,help="发卡时间"),
            "valid_date" : fields.date("valid_date",help="卡有效期"),
            "overdraft_fee" : fields.float("overdraft_fee",digits = (10,2),help="可透支额度"),
            "card_password" : fields.char("card_password",size = 20,required = True,help = "卡密码,不可为空"),
            "phone" : fields.char("phone",size = 20,help="联系电话"),
            "birthday" : fields.date("birthday",help="联系电话"),
            "sex" : fields.selection(helper.sexes_for_select,"sex",help="性别"),
            "id_type" : fields.selection(helper.id_types_for_select,"id_type",help="证件类型"),
            "id_no" : fields.char("id_no",size = 30,help="证件号码"), "v_no" : fields.char("v_no",size = 30,help="车牌号码"),
            "qq" : fields.char("qq",size = 30,help="QQ号码"),
            "email" : fields.char("email",size = 30,help="邮件地址"),
            "company" : fields.char("company",size = 30,help="工作单位"),
            "address" : fields.char("address",size = 60,help="地址"),
            "member_charge_ids" : fields.one2many('member_management.member_charge','member_id',help="会员充值记录"),
            "member_consumption_ids" : fields.one2many('member_management.member_consumption','member_id',help="会员消费记录"),
            "balance": fields.function(_compute_balance_and_points,type='float',multi="compute_fields",string="balance",digits_compute = dp.get_precision('member_management_fee'),help="卡余额"),
            "points": fields.function(_compute_balance_and_points,type='integer',multi="cimpute_fields",string="points",help="卡积分"),
            "card_state" : fields.boolean("state"),
            "active" : fields.boolean("active"),
            'room_fee_discount' : fields.related('member_class_id','room_fee_discount',type='float',string='房费折扣'),
            'drinks_fee_discount' : fields.related('member_class_id','drinks_fee_discount',type='float',string='酒水费折扣'),
            }
    _defaults = {
            "active" : True,
            "card_state" : True,
            "card_fee" : 0.0,
            'up_card_fee' : 0.0,
            "overdraft_fee" : 0.0,
            'begin_datetime' : fields.datetime.now,
            'member_no': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'member_management.member'),
            'balance' : 0.0,
            }

    def calculate_casher_shift_report(self,cr,uid,start_datetime,end_datetime):
        '''
        计算会员卡业务发生情况
        :param start_datetime datetime 业务起始时间
        :param end_datetime datetime 业务结束时间
        :return dict 
                'member_card_count'      新会员数量
                'member_card_fee'   会员卡销售金额
                'member_charge_fee' 会员充值金额
        '''
        pool = self.pool
        #计算新办会员卡数量
        ids = self.search(cr,uid,[('begin_datetime','>=',helper.strftime(start_datetime)),('begin_datetime','<=',helper.strftime(end_datetime))])
        member_card_count = len(ids)
        member_card_fee = 0.0
        for r in self.browse(cr,uid,ids):
          member_card_fee += r.card_fee + r.up_card_fee

        #计算会员充值金额
        charge_fee = 0.0
        charge_ids =  pool.get('member_management.member_charge').search(cr,uid,[('bill_datetime','>=',helper.strftime(start_datetime)), \
            ('bill_datetime','<=',helper.strftime(end_datetime))])
        for r in pool.get('member_management.member_charge').browse(cr,uid,charge_ids):
          charge_fee += r.charge_fee

        return {
            'member_card_count' : member_card_count,
            'new_member_card_fee'   : member_card_fee,
            'member_charge_fee' : charge_fee,
            }
