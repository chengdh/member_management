# -*- coding: utf-8 -*-

from osv import fields, osv
class points_config(osv.osv):
  '''
  积分规则
  '''
  _name = "member_management.points_config"

  _description = "积分规则"

  _columns = {
        "config_prior": fields.integer("config_prior",required = True,help="设置优先级,优先级高的放到前边" ),
        "drinks_fee": fields.float("drinks_fee",digits =(10,2),required = True,help="酒水消费金额" ),
        "drinks_points": fields.integer("drinks_points",required = True,help="酒水费积分" ),
        "room_fee": fields.integer("room_fee",digits = (10,2),required = True,help="房费" ),
        "room_points": fields.float("room_points",required = True,help="房费积分" ),
        "active": fields.boolean("active"),
      }

  _defaults = {
      'active' : True,
      }

  def _calculate_points(self,cr,uid,consume_fee = 0.0,fee_type='room_fee'):
    '''
    根据设定情况计算积分点数
    :param consume_fee float 消费金额
    :param fee_type 费用类型 room_fee 房费 drinks_fee 酒水费
    :return integer 点数
    '''
    if not fee_type or not consume_fee or consume_fee == 0 :
      return 0

    ids = self.search(cr,uid,[],limit = 1,order = 'config_prior DESC')
    config = self.browse(cr,uid,ids[0])
    the_points = 0
    if fee_type == 'room_fee':
      the_points = int(consume_fee/config.room_fee)*config.room_points

    if fee_type == 'drinks_fee':
      the_points = int(consume_fee/config.drinks_fee)*config.drinks_points

    return the_points

  def calculate_room_fee_points(self,cr,uid,consume_room_fee = 0.0):
    '''
    计算房费积分
    '''
    return self._calculate_points(cr,uid,consume_room_fee)

  def calculate_drinks_fee_points(self,cr,uid,consume_drinks_fee = 0.0):
    '''
    计算房费积分
    '''
    points = self._calculate_points(cr,uid,consume_drinks_fee,'drinks_fee')
    return points


