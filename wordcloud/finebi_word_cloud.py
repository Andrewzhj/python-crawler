# -*- coding: UTF-8 -*-
'''
@author: Andrewzhj
@contact: andrew_zhj@126.com
@file: finebi_word_cloud.py
@time: 2018/10/18 10:35
@desc:
@note:
'''
import os
from os import path

import jieba
import numpy
import matplotlib.pyplot as plt
import pymysql
from scipy.misc import imread
import pandas as pd
from wordcloud import WordCloud

db = pymysql.connect("10.1.210.50", "jiang", "jiang", "market", charset='utf8')
cursor = db.cursor()

comment_dir = "comment/"

def show():
    '''
    直接生成图片
    :return:
    '''
    d = path.dirname(__file__)
    # Read the whole text.
    text = open(path.join(d, 'comment/漫游超人.txt')).read()
    cut_text = ' '.join(jieba.cut(text))
    color_mask = imread("demo.png")

    cloud = WordCloud(
            #设置字体，不指定就会出现乱码
            font_path="msyh.ttf",
            #font_path=path.join(d,'simsun.ttc'),
            #设置背景色
            background_color='white',
            #词云形状
            mask=color_mask,
            #允许最大词汇
            max_words=2000,
            #最大号字体
            max_font_size=40
        )
    word_cloud = cloud.generate(cut_text) # 产生词云
    # word_cloud.to_file("result.jpg") #保存图片
    #  显示词云图片
    plt.imshow(word_cloud)
    plt.axis('off')
    plt.show()

def comment_to_db(file_name):
    '''
    读取目录中指定的文件内存，保存到mysql
    :return:
    '''
    d = path.dirname(__file__)
    # Read the whole text.
    text = open(path.join(d, 'comment/' + file_name)).read()
    text = text.replace("\n", "")
    # 使用结巴分词进行中文分词
    segment = jieba.lcut(text)
    words_df = pd.DataFrame({'segment': segment})
    # 去掉停用词
    stopwords = pd.read_csv("stopwords.csv", index_col=False, quoting=3, sep="\t",
                            names=['stopword'], encoding='utf-8')  # quoting=3全不引用
    words_df = words_df[~words_df.segment.isin(stopwords.stopword)]
    # 统计词频
    words_stat = words_df.groupby(by=['segment'])['segment'].agg({"count": numpy.size})
    words_stat = words_stat.reset_index().sort_values(by=["count"], ascending=False)
    word_frequence = {x[0]: x[1] for x in words_stat.head(1000).values}
    # print(word_frequence)
    producer = str(file_name).split(".")[0]
    for key, value in word_frequence.items():
        save_to_db(producer, str(key), str(value))

def save_to_db(producer, word, word_count):
    sql = "INSERT INTO ctrip_comment (producer, word, word_count) VALUES ('%s', '%s', '%s')"  %(producer, word, word_count)
    executeSQL(sql)

def executeSQL(sql):
    cursor.execute(sql)
    db.commit()

def loog_dir():
    files = os.listdir(comment_dir)
    for file in files:
        comment_to_db(file)

if __name__ == '__main__':
    # show()
    # comment_to_db()
    loog_dir()