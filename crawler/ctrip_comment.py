# -*- coding: UTF-8 -*-
'''
@author: Andrewzhj
@contact: andrew_zhj@126.com
@file: ctrip_comment.py
@time: 2018/10/15 14:08
@desc:
@note:
'''
import requests
from bs4 import BeautifulSoup
import re
import time

'''
https://blog.csdn.net/qq_34777600/article/details/77460380
'''

session = requests.Session()

def fetch_page_count():
    '''
    获取携程  出境wifi 商品页总页数
    :return:
    '''
    url = "http://huodong.ctrip.com/wifi/search/?keyword=&filters=c48"
    response = session.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text,'lxml')
        page_info = soup.find_all(attrs={"class": "c_page2_numtop"})
        page_arr = (page_info[0].string).split('/')
        page_count = re.findall(r"\d+\.?\d*", str(page_arr[1]))[0]
        print('总页数： {}'.format(page_count))
        return page_count
    return 0

def fetch_page_item(page_index):
    url = 'http://huodong.ctrip.com/wifi/search/?keyword=&filters=c48p' + str(page_index)
    response = session.get(url)
    if response.status_code == 200:
        print("Page Index: %s" % page_index)
        loop_all_item(response.text)

def loop_all_item(html):
    soup = BeautifulSoup(html, 'lxml')
    produce_mod_a = soup.select('a.product_mod')
    for mod in produce_mod_a:
        itemId = ''
        a_href_arr = str(mod['href']).split("/")
        if len(a_href_arr) == 3:
            itemId = re.findall(r"\d+", str(a_href_arr[2]))[0]
            print(itemId)
        title = str(mod.select('h2.ttd-flex > span.product_title')[0].get_text()).strip()
        producer = str(mod.select('div.product_info > span.mr_25 > em')[0].get_text()).strip()
        comment_info = str(mod.select('div.product_info > span.product_comment')[0].get_text()).strip()
        comment_count = int(re.findall(r"\d+", str(comment_info))[0])
        if itemId.strip() == '':
            continue

def fetch_comment():
    url = "http://huodong.ctrip.com/Activity-Booking-OnlineWebSite/Recommend/UserComments?id=10037247&productName=欧洲49国WiFi租赁（上海自取 全程高速不降速）&pageSize=5&pageIndex=1"
    re = session.get(url);
    if re.status_code == 200:
        soup = BeautifulSoup(re.text, 'lxml')
        [s.extract() for s in soup(['h4', 'span'])]
        comments = soup.select("div.ticket_user_left")
        for comment in comments:
            print(comment.get_text().strip())

def fetch():
    try:
        totalPage = int(fetch_page_count()) + 1
        for i in range(1, totalPage):
            fetch_page_item(i)
            time.sleep(2)
    except Exception as e:
        print("error: %s" % e)

if __name__ == '__main__':
    fetch()