# -*- coding: UTF-8 -*-
'''
@author: Andrewzhj
@contact: andrew_zhj@126.com
@file: SIMCount.py
@time: 2018/9/10 17:19
@desc:
@note:
'''
import datetime
import json
import time

from sycm import Config as config
from sycm.Common import Common
import urllib.parse
import urllib.request
import xlwt

_country = {
    "香港": "27369",
    "日本": "27023",
    "韩国": "27019",
    "台湾": "27368",
    "泰国": "27024",
    "新加坡": "43446",
    "马来西亚": "3286452",
    "澳门": "29121",
    "印度尼西亚": "3355806",
    "欧洲": "29148"
}

_item = {
    "亿点": "8940440",
    "中国移动（港澳台）": "1065228016",
    "游惠宝": "243468511",
}

''' 
    电话卡数据爬取
    页面数据：
        登录生意参谋（选择旧版本）
        进入菜单：市场 -> 属性分析
        设定查询条件: 境外电话卡/手机卡   国家/地区
    存在问题：
        点击“日本”进入子菜单，找不到完整的菜单刷新接口，故不能深度爬取。
    本脚本指定国家、通信运营商调用对应的接口查询。
'''
class SIMCount(object):
    def __init__(self):
        self._user = config.LOGIN_USER
        self._header = config.HEADER

    def fetch(self):
        '''
        查询三个通讯运营商下10个国家的数据，保存到excel
        :return:
        '''
        for (itemKey, itemValue) in _item.items():
            excel = xlwt.Workbook()
            try:
                for (countryKey, countryValue) in _country.items():
                    _url = "https://sycm.taobao.com/mq/property/property.json?cateId=125352005&dateRange=2018-09-10%7C2018-09-10&dateType=recent1&device=0&propertyIds=15438105|155792781&propertyValueIds=" + itemValue + "|" + countryValue + "&seller=-1&token=5cd7e707a&_=1536651771484"
                    req_data = urllib.parse.urlencode(self._user).encode('utf-8')
                    _req = urllib.request.Request(_url, data=req_data, headers=self._header)
                    with urllib.request.urlopen(_req) as response:
                        _json = json.loads(response.read().decode('utf-8'))
                        data = _json['content']['data']['data']
                        sheet_name = itemKey + "-" + countryKey
                        self.inputEXCEL(excel, sheet_name, data)
                    time.sleep(2)
            except Exception as e:
                print(e)
            finally:
                excel.save('E:\\通讯运营商卡的市场分析.xls')

    def fetch2(self):
        '''
        查询10个国家下支付的订单数，保存到excel
        :return:
        '''
        excel = xlwt.Workbook()
        try:
            for (countryKey, countryValue) in _country.items():
                _url = "https://sycm.taobao.com/mq/property/property.json?cateId=125352005&dateRange=2018-09-10%7C2018-09-10&dateType=recent1&device=0&propertyIds=155792781&propertyValueIds="+ countryValue +"&seller=-1&token=5cd7e707a&_=1536660484648"
                req_data = urllib.parse.urlencode(self._user).encode('utf-8')
                _req = urllib.request.Request(_url, data=req_data, headers=self._header)
                with urllib.request.urlopen(_req) as response:
                    _json = json.loads(response.read().decode('utf-8'))
                    data = _json['content']['data']['data']
                    sheet_name = countryKey
                    self.inputEXCEL(sheet_name, data)
                time.sleep(2)
        except Exception as e:
            print(e)
        finally:
            excel.save('E:\\卡的市场分析.xls')

    def inputEXCEL(self, excel, sheet_name, data):
        '''
        数据写入到excel
        :param excel:
        :param sheet_name:
        :param data:
        :return:
        '''
        sheet = excel.add_sheet(sheet_name)
        for sim in data:
            indexCode = sim['indexCode']
            if indexCode == "paySubOrderCnt":
                row = 0
                current_date = Common.now_date_time()
                for i in range(0, len(sim["range"]))[::-1]:
                    current_date += datetime.timedelta(days=-1)
                    sheet.write(row, i, Common.format_date(current_date))
                    print("write date: %s" % Common.format_date(current_date))
                row += 1
                column = 0
                for i in sim['range']:
                    sheet.write(row, column, i)
                    column += 1

if __name__ == '__main__':
    simCount = SIMCount()
    simCount.fetch()
    simCount.fetch2()
