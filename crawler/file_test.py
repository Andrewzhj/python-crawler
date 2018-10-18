# -*- coding: UTF-8 -*-
'''
@author: Andrewzhj
@contact: andrew_zhj@126.com
@file: file_test.py
@time: 10/17/18 11:47 AM
@desc:
@note:
'''
import os

dir_path = '../wordcloud/comment'

def test():
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    file_path =dir_path + "/漫游超人.txt"
    if not os.path.exists(file_path):
        f = open(file_path, 'w')
    else:
        f = open(file_path, 'a')
    for i in range(10):
        f.write(str(i) + '\n')
    f.close()

def loog_dir():
    files = os.listdir(dir_path)
    for file in files:
        file_name = file.split(".")[0]
        print(file_name)

if __name__ == '__main__':
    # test()
    loog_dir()