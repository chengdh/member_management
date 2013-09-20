# -*- coding: utf-8 -*-
#打折卡 不记名
from osv import fields, osv

class discount_card(osv.osv):
    '''打折卡信息设置'''
    _name = "member_management.discount_card"
    _descripton = "打折卡"

    _rec_name = "card_no"

    _columns ={
            "card_no" : fields.char("card_no",size = 30,readonly = True,select = True,help="卡号",required = True),
            "discount_card_type_id" : fields.many2one("member_management.discount_card_type","discount_card_type_id",required = True,select = True,help="打折卡类别"),
            "card_fee" : fields.float("card_fee",digits =  (10,2),help = "制卡费用,默认取打折卡类别中的制卡费用"),
            "valid_date" : fields.date("valid_date",help="卡有效期"),
            'room_fee_discount' : fields.related('discount_card_type_id','room_fee_discount',string='房费折扣'),
            'drinks_fee_discount' : fields.related('discount_card_type_id','drinks_fee_discount',string='酒水费折扣'),
            "active" : fields.boolean("active"),
            }

    _defaults = {
            "card_fee" : 0,
            'active' : True
            }

