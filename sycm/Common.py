# -*- coding: UTF-8 -*-
'''
@author: Andrewzhj
@contact: andrew_zhj@126.com
@file: Common.py
@time: 2018/8/30 19:27
@desc:
@note:
'''
import calendar
import datetime

class Common(object):

    def __init__(self):
        pass

    @staticmethod
    def format_date(date_time):
        return date_time.strftime('%Y-%m-%d')

    @staticmethod
    def now_date_time():
        return datetime.datetime.now()

    @staticmethod
    def get_date_time(str_date_time):
        return datetime.datetime.strptime(str_date_time, '%Y-%m-%d')

    @staticmethod
    def get_last_6_date(sunday_date):
        return sunday_date + datetime.timedelta(days=-6)

    @staticmethod
    def get_fetch_date():
        return Common.now_date_time().strftime('%Y-%m-%d')

    @staticmethod
    def last_day_date(current_date):
        return current_date + datetime.timedelta(days=-1)

    @staticmethod
    def get_last_saturday():
        currentDay = datetime.datetime.today()
        while currentDay.weekday() != calendar.SATURDAY:
            currentDay -= datetime.timedelta(days=-1)
        return currentDay

    @staticmethod
    def get_last10_day():
        current_date = datetime.datetime.today()
        return current_date + datetime.timedelta(days=-10)

    @staticmethod
    def get_future10_day():
        current_date = datetime.datetime.today()
        return current_date + datetime.timedelta(days=10)

if __name__ == '__main__':
    currentTime = Common.get_last10_day()
    print(currentTime)
    print(str(round(currentTime.timestamp())))
    currentTime = Common.get_future10_day()
    print(currentTime)
    print(str(round(currentTime.timestamp())))

