# -*- coding: UTF-8 -*-
'''
@author: Andrewzhj
@contact: andrew_zhj@126.com
@file: ctrip_comment.py
@time: 2018/10/15 14:08
@desc: 爬取 移动wifi 评论数据，保存到 mongodb
@note:
'''
import requests
from bs4 import BeautifulSoup
import re
import time
import os

session = requests.Session()
from pymongo import MongoClient
conn = MongoClient('localhost', 27017)
ctrip_db = conn.ctrip


def fetch_page_count():
    '''
    获取携程  出境wifi 商品页总页数
    :return:
    '''
    url = "http://huodong.ctrip.com/wifi/search/?keyword=&filters=c48"
    response = session.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text,'html.parser')
        page_info = soup.find_all(attrs={"class": "c_page2_numtop"})
        page_arr = (page_info[0].string).split('/')
        page_count = re.findall(r"\d+\.?\d*", str(page_arr[1]))[0]
        print('总页数： {}'.format(page_count))
        return page_count
    return 0

def fetch_page_item(page_index):
    '''
    抓取每页商品信息
    :param page_index:
    :return:
    '''
    url = 'http://huodong.ctrip.com/wifi/search/?keyword=&filters=c48p' + str(page_index)
    response = session.get(url)
    if response.status_code == 200:
        print("Page Index: %s" % page_index)
        loop_all_item(response.text)

def save_comment(producer, comment):
    '''
    保存评论信息
    :param producer:
    :param comment:
    :return:
    '''
    ctrip_db.comment.save({"producer": producer, "comment": comment})

def loop_all_item(html):
    '''
    抓取详细信息
    :param html:
    :return:
    '''
    soup = BeautifulSoup(html, 'html.parser')
    produce_mod_a = soup.select('a.product_mod')
    for mod in produce_mod_a:
        itemId = ''
        a_href_arr = str(mod['href']).split("/")
        if len(a_href_arr) == 3:
            itemId = re.findall(r"\d+", str(a_href_arr[2]))[0]
        title = str(mod.select('h2.ttd-flex > span.product_title')[0].get_text()).strip()
        producer = str(mod.select('div.product_info > span.mr_25 > em')[0].get_text()).strip()
        comment_info = str(mod.select('div.product_info > span.product_comment')[0].get_text()).strip()
        comment_total = 0

        try:
            comment_total = int(re.findall(r"\d+", str(comment_info))[0])
        except Exception as e:
            print(e)

        print("comment_total: %s" % comment_total)
        if itemId.strip() == '':
            continue
        if comment_total == 0:
            continue

        comment_count = 0
        page_index = 1
        page_size = 50
        while(comment_count < comment_total):
            fetch_comment(producer, itemId, title, page_size, page_index)
            page_index += 1
            comment_count = comment_count + page_size
            time.sleep(1)
            # print("comment_total: %s, comment_count: %s"  %(str(comment_total), str(comment_count)))
        return


def save_comment_to_file(producer, cleaned_comments):
    dir_path = './comment'
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    file_path =dir_path + "/" + producer + ".txt"
    if not os.path.exists(file_path):
        f = open(file_path, 'w')
    else:
        f = open(file_path, 'a')
    f.write(str(cleaned_comments) + '\n')
    f.close()


def fetch_comment(producer, itemId, title, page_size, page_index):
    '''
    抓取评论，并保存到mongodb
    :param producer:
    :param itemId:
    :param title:
    :param page_size:
    :param page_index:
    :return:
    '''
    url = "http://huodong.ctrip.com/Activity-Booking-OnlineWebSite/Recommend/UserComments?id=" + str(itemId) + \
          "&productName=" + str(title) + "&pageSize=" + str(page_size) + "&pageIndex=" + str(page_index)
    response = session.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup)
        [s.extract() for s in soup(['h4', 'span', 'p'])]
        comments = soup.select("div.ticket_user_left")
        for comment in comments:
            pattern = re.compile(r'[\u4e00-\u9fa5]+')
            filterdata = re.findall(pattern, comment.get_text().strip())
            cleaned_comments = ''.join(filterdata)
            # save_comment(producer, cleaned_comments)
            save_comment_to_file(producer, cleaned_comments)

def fetch():
    '''
    评论抓取入口
    :return:
    '''
    try:
        totalPage = int(fetch_page_count()) + 1
        for i in range(1, totalPage):
            fetch_page_item(i)
            time.sleep(2)
    except Exception as e:
        print("error: %s" % e)

if __name__ == '__main__':
    fetch()