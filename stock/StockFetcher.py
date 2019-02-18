# -*- coding: UTF-8 -*-
'''
@author: Andrewzhj
@contact: andrew_zhj@126.com
@file: StockFetcher.py
@time: 1/3/19 10:54 PM
@desc:
@note:
'''

import requests
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup


class StockFetcher(object):
    def __init__(self):
        self.url = "http://quote.eastmoney.com/stocklist.html"
        self.session = requests.Session()


    def stockeList(self):
        response = self.session.get(self.url)
        response.encoding='GBK'
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            html = soup.select("div.qox > div.quotebody")
            for x in html[0].find_all('li'):
                print(x)

    def stockeDetail(self):
        url = "http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?rtntype=5&token=4f1862fc3b5e77c150a2b985b12db0fd&cb=jQuery18308531276643182979_1546666707617&id=3007452&type=k&authorityType=&_=1546666741955"
        


if __name__ == '__main__':
    fetcher = StockFetcher()
    fetcher.stockeList()