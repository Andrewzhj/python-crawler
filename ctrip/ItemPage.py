# -*- coding: UTF-8 -*-
'''
@author: Andrewzhj
@contact: andrew_zhj@126.com
@file: ItemPage.py
@time: 2018/10/15 16:28
@desc:
@note:
'''
from bs4 import BeautifulSoup
from ctrip.Common import Common
import re

import sys
sys.path.append("../")

class ItemPage(object):
    def __init__(self):
        self.session = Common.getRequestSession()

    def fetch_page_count(self):
        '''
        获取携程  出境wifi 商品页总页数
        :return:
        '''
        url = "http://huodong.ctrip.com/wifi/search/?keyword=&filters=c48"
        response = self.session.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            page_info = soup.find_all(attrs={"class": "c_page2_numtop"})
            page_arr = (page_info[0].string).split('/')
            page_count = re.findall(r"\d+\.?\d*", str(page_arr[1]))[0]
            print('总页数： {}'.format(page_count))
            return page_count
        return 0

if __name__ == '__main__':
    itemPage = ItemPage()
    itemPage.fetch_page_count()