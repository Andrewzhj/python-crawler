# -*- coding: UTF-8 -*-
'''
@author: Andrewzhj
@contact: andrew_zhj@126.com
@file: MongoTest.py
@time: 10/16/18 3:10 PM
@desc:
@note:
'''

from pymongo import MongoClient

conn = MongoClient('localhost', 27017)
ctrip_db = conn.ctrip

comment_list = ctrip_db.comment.find()
# curse = comment_list.fetch(10)
for o in comment_list:
    print(o)
