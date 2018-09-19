# -*- coding: UTF-8 -*-
# -*- coding: UTF-8 -*-
'''
@author: Andrewzhj
@contact: andrew_zhj@126.com
@file: excel_to_db.py
@time: 2018/8/31 11:45
@desc:
@note:
'''
import pymysql

db = pymysql.connect("10.1.210.50", "jiang", "jiang", "market", charset='utf8')
cursor = db.cursor()
import xlrd

'''
读取方洲的原始数据，并入库
商品信息变动较大，套餐分组需确认，仅添加了前两周的数据
'''

def executeSQL(sql):
    cursor.execute(sql)
    db.commit()

def close():
    cursor.close()
    db.close()

#路径前加 r，读取的文件路径
# file_path = r'Z:\\方洲\\周一报告\\180806\\生意参谋数据180806.xlsx'
# cmDate = '2018-08-01'

# file_path = r'Z:\\方洲\\周一报告\\180730\\生意参谋数据180730.xlsx'
# cmDate = '2018-07-28'

file_path = r'Z:\\方洲\\周一报告\\180723\\生意参谋数据180723.xlsx'
cmDate = '2018-07-20'

#文件路径的中文转码
# file_path = file_path.decode('utf-8')

#获取数据
data = xlrd.open_workbook(file_path)

#获取sheet
table = data.sheet_by_name('热销商品榜-属性粒度')

#获取总行数
nrows = table.nrows
#获取总列数
ncols = table.ncols

_sql = "INSERT INTO sycm_item_trend (itemTitle, shopName, producer, payOrdCnt, payItemQty, cmDate, fetchDate) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')"
for i in range(1, nrows):
    row_value = table.row_values(i)
    itemInfo = str(row_value[0]).split("价格：")
    itemTitle = str(itemInfo[0])
    # price = itemInfo[1]
    shopName = row_value[1]
    payOrdCnt = row_value[2]
    payItemQty = row_value[3]
    producer = row_value[4]
    sql = _sql % (itemTitle, shopName, producer, payOrdCnt, payItemQty, cmDate, cmDate)
    # print(sql)
    executeSQL(sql)
close()
