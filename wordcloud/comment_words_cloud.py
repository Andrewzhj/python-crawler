# -*- coding: UTF-8 -*-
'''
@author: Andrewzhj
@contact: andrew_zhj@126.com
@file: comment_words_cloud.py
@time: 10/16/18 3:53 PM
@desc: 提取评论数据，进行热词展示
@note:
'''

import jieba
from wordcloud import WordCloud, ImageColorGenerator
import pandas as pd
from pymongo import MongoClient
import numpy
from PIL import Image
import matplotlib.pyplot as plt
import os

'''
https://blog.csdn.net/qq_34777600/article/details/77460380
'''

conn = MongoClient('localhost', 27017)
ctrip_db = conn.ctrip

def word_cloud():
    producer_list = ctrip_db.comment.find().distinct("producer")
    print(producer_list)
    for producer in producer_list:
        comment_list = ctrip_db.comment.find({"producer": str(producer)})
        words_df = pd.DataFrame()
        for o in comment_list:
            segment = jieba.lcut(str(o['comment']))
            words_df = words_df.append(pd.DataFrame({str(producer): segment}), sort=True)

        # 去掉停用词
        stopwords = pd.read_csv("stopwords.csv", index_col=False, quoting=3, sep="\t", names=['stopword'],
                                encoding='utf-8')  # quoting=3全不引用
        words_df = words_df[~words_df[str(producer)].isin(stopwords.stopword)]
        words_stat = words_df.groupby(by=[str(producer)])[str(producer)].agg({numpy.size})
        words_stat.columns = ['计数']
        words_stat = words_stat.reset_index().sort_values(by=["计数"], ascending=False)
        # print(words_stat.head(100))
        print("---------分割线-----------")
        bg_pic = numpy.array(Image.open("test.jpg"))
        # 用词云进行显示
        word_cloud = WordCloud(
            font_path="msyh.ttf",
            background_color="white",
            max_font_size=80,
            width=2000,
            height=1800,
            mask=bg_pic,
            mode="RGBA",
            margin=2
        )
        word_frequence = {x[0]: x[1] for x in words_stat.head(1000).values}
        # print(word_frequence)
        """
        word_frequence_list = []
        for key in word_frequence:
            temp = (key, word_frequence[key])
            word_frequence_list.append(temp)
            #print(word_frequence_list)
        """
        word_cloud = word_cloud.fit_words(word_frequence)

        image_colors = ImageColorGenerator(bg_pic)  # 根据图片生成词云颜色

        # plt.imshow(word_cloud)  # 显示词云图片
        # plt.axis("off")
        # plt.show()

        dir_path = "./result"
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        file_name = dir_path + "/" + producer + '.png'
        word_cloud.to_file(file_name)  # 把词云保存下来
        # return


if __name__ == '__main__':
    word_cloud()