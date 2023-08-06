# -*- coding: utf-8 -*-

# author: 'ileona'
# date: 2021/7/3 15:57

import time
import datetime

year = '%Y'
month = '%Y-%m'
day = '%Y-%m-%d'
hours = '%Y-%m-%d %H'
minutes = '%Y-%m-%d %H:%M'
seconds = '%Y-%m-%d %H:%M:%S'


def unixTime(string, dateFormat):
    """
    将日期转换为时间戳
    :param string:
    :param dateFormat:
    :return:
    """
    # 转换成时间数组
    timeArray = time.strptime(string, dateFormat)
    # 转换成时间戳
    timestamp = int(time.mktime(timeArray))
    return timestamp


def customTime(timestamp, dateFormat='%Y-%m-%d %H:%M:%S'):
    """
    将时间戳转为日期 dateFormat默认
    :param timestamp:
    :param dateFormat:
    :return:
    """
    # 转换成localtime
    time_local = time.localtime(timestamp)
    # 转换成新的时间格式(2016-05-05 20:28:54)
    dt = time.strftime(dateFormat, time_local)
    return dt


def dateToTimestamp(date):
    dayStr = date.strftime(day)
    return unixTime(dayStr, day)


def getCurrTime():
    """
    获取当前时间戳 秒
    :return:
    """
    return int(time.time())


def getCurrTimeOfMs():
    """
    获取当前时间戳 毫秒
    :return:
    """
    return int(time.time() * 1000)


def getTheDay():
    """
    获取当前日期
    :return:
    """
    return customTime(getCurrTime(), day)


def getDay(timeStamp=None):
    """
    获取日期对象 默认当天
    :param timeStamp:
    :return:
    """
    return datetime.datetime.utcfromtimestamp(timeStamp) if timeStamp else datetime.datetime.today()


def getStartOfDay(timeStamp=None):
    """
    获取一天开始时间戳 默认当天
    :param timeStamp:
    :return:
    """
    if timeStamp:
        return unixTime(customTime(timeStamp, day), day)
    return unixTime(getTheDay(), day)


def getEndOfDay(timeStamp=None):
    """
    获取一天结束时间戳 默认当天
    :param timeStamp:
    :return:
    """
    return getStartOfDay(timeStamp) + 86400 - 1


def getStartOfWeek(timeStamp=None):
    """
    获取一周的开始时间戳 默认：本周
    :param timeStamp:
    :return:
    """
    data = getDay(timeStamp)
    startWeek = data - datetime.timedelta(days=data.isoweekday() - 1)
    return dateToTimestamp(startWeek)


def getEndOfWeek(timeStamp=None):
    """
    获取一周的结束时间戳 默认：本周
    :param timeStamp:
    :return:
    """
    return getStartOfWeek(timeStamp) + 7 * 86400 - 1


def getStartOfMonth(timeStamp=None):
    data = getDay(timeStamp)
    startMonth = datetime.date(data.year, data.month, 1)
    return dateToTimestamp(startMonth)


def getEntOfMonth(timeStamp=None):
    data = getDay(timeStamp)
    if data.month == 12:
        yearInt, monthInt = data.year + 1, data.month
    else:
        yearInt, monthInt = data.year, data.month + 1
    startMonth = datetime.date(yearInt, monthInt, 1)
    return dateToTimestamp(startMonth) - 1


def getStartOfYear(timeStamp=None):
    data = getDay(timeStamp)
    startMonth = datetime.date(data.year, 1, 1)
    return dateToTimestamp(startMonth)


def getEndOfYear(timeStamp=None):
    data = getDay(timeStamp)
    startMonth = datetime.date(data.year + 1, 1, 1)
    return dateToTimestamp(startMonth) - 1