# -*- coding: utf-8 -*-
import decimal_precision as dp
from osv import fields
from datetime import date,datetime,time,timedelta
import openerp.tools as tools
import logging
_logger = logging.getLogger(__name__)
#时间段选择
def time_for_selection(self,cr,uid,context = None):
     ret = [("%02i:00" % i,"%02i时30分" % i) for i in range(24)] + [("%02i:30" % i,"%02i时00分" % (i+1)) for i in range(24)]
     ret.sort()
     ret.pop()
     ret.append(("23:59","23时59分"))
     return ret

#男女
def sexes_for_select(self,cr,uid,context = None):
    ret=[("F","女"),("M","男")]
    return ret
#证件类型
def id_types_for_select(self,cr,uid,context = None):
    ret=[(1,"身份证"),(2,"驾驶证"),(3,"其他证件")]
    return ret

#根据0 1 2 3 4 5 6 分别返回星期缩写 min =0 ~ sun= 6
def weekday_str(weekday_int):
    weekday_dict = {
            0 : 'mon',
            1 : 'tue',
            2 : 'wed',
            3 : 'thu',
            4 : 'fri',
            5 : 'sat',
            6 : 'sun'
            }
    return weekday_dict[weekday_int]

def current_user_tz(obj,cr,uid,context = None):
    """
    获取当前登录用户的时区设置
    :param cursor cr 数据库游标
    :params integer uid 当前登录用户id
    """
    the_user = obj.pool.get('res.users').read(cr,uid,uid,['id','tz','name'])
    return the_user['tz']

def user_context_now(obj,cr,uid):
    """
    获取当前登录用户的本地日期时间
    :return 本地化的当前日期
    """
    tz = current_user_tz(obj,cr,uid)
    context_now = fields.datetime.context_timestamp(cr,uid,datetime.now(),{"tz" : tz})
    return context_now

def float_time_to_datetime(float_time,base_datetime = None):
    """
    将以float方式形式存储的time字段值转换为datetime,
    :param float_time float float方式存储的time字段值
    :param base_datetime 参照的datetime
    :return datetime UTC 当日日期 + time
    """
    now=datetime.now()
    h=int(float_time)
    m=int((float_time-h)*60)
    datetime_time=datetime(year= base_datetime.year if base_datetime else now.year, \
        month = base_datetime.month if base_datetime else now.month, \
        day = base_datetime.day if base_datetime else now.day, \
        hour=h,minute=m)
    return datetime_time

def timedelta_minutes(datetime_from,datetime_to):
    '''
    计算给定两个时间的相差分钟数
    :param datetime_from datetime 起始时间
    :param datetime_to datetime 结束时间

    :return integer 两个时间的相差分钟数
    '''
    return int((datetime_to - datetime_from).total_seconds()/60)

def str_timedelta_minutes(datetime_from_str,datetime_to_str):
    '''
    计算给定两个时间的相差分钟数
    :param datetime_from_str string 起始时间
    :param datetime_to_str string 结束时间

    :return integer 两个时间的相差分钟数
    '''
    return int((strptime(datetime_to_str) - strptime(datetime_from_str)).total_seconds()/60)



def float_time_minutes_delta(float_time_from,float_time_to):
    '''
    计算给定两个时间的相差分钟数
    因为全部使用UTC时间存储,所以可能存在float_time_to < float_time_from的情况,这种情况下,
    float_time_to加1天
    :param float_time_from float 形式是18.09,指的是起始时间
    :param float_time_to float 形式是21.30,指的是结束时间时间

    :return integer 两个时间的相差分钟数
    '''
    time_from = float_time_to_datetime(float_time_from)
    time_to = float_time_to_datetime(float_time_to)
    #判断是否time_to < time_from
    if time_to < time_from:
        time_to = time_to + timedelta(days = 1)
    return int((time_to - time_from).total_seconds()/60)

def utc_time_between(float_time_from,float_time_to,cur_time):
    """
    判断给定的时间字符串是否在给定的时间区间内
    由于对时间统一采用UTC时间保存,可能存在time_to < time_from的情况
    :params float float_time_from 形式类似 9.1的时间字符串
    :params float float_time_to 形式类似 9.2的时间字符串
    :params datetime cur_time 要比较的datetime
    :return True 在范围内 else False
    """
    time_from = float_time_to_datetime(float_time_from,base_datetime = cur_time)
    time_to = float_time_to_datetime(float_time_to,base_datetime = cur_time)
    #判断是否time_to < time_from
    #采用UTC时间,可能存在跨天的情况
    if time_to < time_from:
        time_to = time_to + timedelta(days = 1)

    return cur_time >= time_from and cur_time <= time_to


def calculate_present_minutes(buy_minutes,promotion_buy_minutes = 0,promotion_present_minutes = 0):
    """
    根据给定的参数计算赠送时长
    买钟时间(分钟数) / 设定买钟时长(分钟数) * 赠送时长
    :params buy_minutes integer 买钟时间
    :params promotion_buy_minutes integer 买钟优惠设置中设定的买钟时长
    :params promotion_present_minutes integer 买钟优惠设置中设定的赠送时长
    :return integer 赠送时长
    """
    #如果未设置优惠信息,则不赠送,直接返回0
    if  not promotion_buy_minutes or buy_minutes < promotion_buy_minutes:
        return 0

    present_minutes = buy_minutes / promotion_buy_minutes * promotion_present_minutes

    return present_minutes

def strptime(str_datetime):
    """
    以服务器端的格式格式化字符串为datetime类型
    :params str_datetime string 日期字符串 required
    :return datetime
    """
    return datetime.strptime(str_datetime,tools.DEFAULT_SERVER_DATETIME_FORMAT)

def strftime(dt):
    """
    以服务端的格式格式化日期对象
    """
    return dt.strftime(tools.DEFAULT_SERVER_DATETIME_FORMAT)

def utc_now_str():
    """
    返回服务默认格式的utc 时间字符串
    """
    return strftime(datetime.now())

def float_round(cr,f_val,application = None):
    """
    使用decimal precision 设置member_management_fee,四舍五入给定的float
    """
    dp_name = application if application else "member_management_fee"
    dp_compute = dp.get_precision(dp_name)

    precision,scale = dp_compute(cr)

    ret = tools.float_round(f_val,precision_digits=scale)
    return ret

