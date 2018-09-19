# -*- coding: UTF-8 -*-
'''
@author: Andrewzhj
@contact: andrew_zhj@126.com
@file: PackageGroup.py
@time: 2018/8/31 12:41
@desc:
@note:
'''

import sys
sys.path.append("../")

import pymysql
import sycm.Config as config

sycm_package_list_sql = [
    "UPDATE sycm_item_trend SET package_name='亚洲其他' WHERE itemTitle LIKE '%亚洲通用%' \
OR itemTitle LIKE '%印度%' \
OR itemTitle LIKE '%尼泊尔%' \
OR itemTitle LIKE '%外蒙古%' \
OR itemTitle LIKE '%以色列%' \
OR itemTitle LIKE '%哈萨克斯坦%' \
OR itemTitle LIKE '%吉尔吉斯斯坦%' \
OR itemTitle LIKE '%亚洲%'",
    "UPDATE sycm_item_trend SET package_name='全球' WHERE itemTitle REGEXP '[0-9]国通用' \
OR itemTitle LIKE '%毛里求斯%' \
OR itemTitle LIKE '%巴西%' \
OR itemTitle LIKE '%肯尼亚%' \
OR itemTitle LIKE '%南非%' \
OR itemTitle LIKE '%摩洛哥%' \
OR itemTitle LIKE '%土耳其%' \
OR itemTitle LIKE '%希腊%' \
OR itemTitle LIKE '%斐济%' \
OR itemTitle LIKE '%摩洛哥%' \
OR itemTitle LIKE '%墨西哥%' \
OR itemTitle LIKE '%突尼斯%' \
OR itemTitle LIKE '%全球%' \
OR itemTitle LIKE '%阿根廷%' \
OR itemTitle LIKE '%尼日利亚%' \
OR itemTitle LIKE '%秘鲁%' \
OR itemTitle LIKE '%约旦%' \
OR itemTitle LIKE '%克罗地亚%' \
OR itemTitle LIKE '%大溪地%' \
OR itemTitle LIKE '%巴基斯坦%' \
OR itemTitle LIKE '%美洲%' \
OR itemTitle LIKE '%多国wifi%' \
OR itemTitle LIKE '%瑙鲁%' \
OR itemTitle LIKE '%捷克%' \
OR itemTitle LIKE '%孟加拉国%' \
OR itemTitle LIKE '%阿尔及利亚%' \
OR itemTitle LIKE '%全航程网络%' \
OR itemTitle LIKE '%乌兹别克斯坦%' \
OR itemTitle LIKE '%多国通用%' \
OR itemTitle LIKE '%坦桑尼亚%'",
    "UPDATE sycm_item_trend SET package_name='台湾' WHERE itemTitle LIKE '%台湾%' \
OR country_name='台湾' \
OR itemTitle LIKE '%台湾%'",
    "UPDATE sycm_item_trend SET package_name='韩国' WHERE itemTitle LIKE '%韩国%' \
OR country_name='韩国' \
OR country_name='韩国'",
    "UPDATE sycm_item_trend SET package_name='日本' WHERE itemTitle LIKE '%日本%' \
OR country_name='日本' \
OR itemTitle LIKE '%日韩%'",
    "UPDATE sycm_item_trend SET package_name='欧洲' WHERE itemTitle LIKE '%欧洲%' \
OR itemTitle LIKE '%英国%' \
OR itemTitle LIKE '%冰岛%' \
OR itemTitle LIKE '%意大利%' \
OR itemTitle LIKE '%瑞士%' \
OR itemTitle LIKE '%瑞典%' \
OR itemTitle LIKE '%德国%' \
OR itemTitle LIKE '%西班牙%' \
OR itemTitle LIKE '%奥地利%' \
OR itemTitle LIKE '%乌克兰%' \
OR itemTitle LIKE '%爱尔兰%' \
OR itemTitle LIKE '%匈牙利%' \
OR itemTitle LIKE '%芬兰%' \
OR itemTitle LIKE '%荷兰%' \
OR itemTitle LIKE '%法国%'",
    "UPDATE sycm_item_trend SET package_name='中港澳' WHERE itemTitle LIKE '%中港澳%' \
OR itemTitle LIKE '%香港%' \
OR itemTitle LIKE '%澳门%' \
OR itemTitle LIKE '%港澳%' \
OR itemTitle LIKE '%国内%'",
    "UPDATE sycm_item_trend SET package_name='泰国' WHERE itemTitle LIKE '%泰国%'",
    "UPDATE sycm_item_trend SET package_name='东南亚' WHERE itemTitle LIKE '%东南亚%' \
OR itemTitle LIKE '%新加坡%' \
OR itemTitle LIKE '%菲律宾%' \
OR itemTitle LIKE '%印尼%' \
OR itemTitle LIKE '%马来西亚%' \
OR itemTitle LIKE '%柬埔寨%' \
OR itemTitle LIKE '%老挝%' \
OR itemTitle LIKE '%缅甸%'",
    "UPDATE sycm_item_trend SET package_name='越南' WHERE itemTitle LIKE '%越南%'",
    "UPDATE sycm_item_trend SET package_name='埃及阿联酋' WHERE itemTitle LIKE '%阿联酋%' \
OR itemTitle LIKE '%埃及%' \
OR itemTitle LIKE '%迪拜%'",
    "UPDATE sycm_item_trend SET package_name='澳新' WHERE itemTitle LIKE '%澳新%' \
OR itemTitle LIKE '%澳大利亚%' \
OR itemTitle LIKE '%新西兰%' \
OR itemTitle LIKE '%澳洲%'",
    # "UPDATE sycm_item_trend SET package_name='以色列' WHERE itemTitle LIKE '%以色列%'",
    "UPDATE sycm_item_trend SET package_name='马尔代夫' WHERE itemTitle LIKE '%马尔代夫%'",
    "UPDATE sycm_item_trend SET package_name='斯里兰卡' WHERE itemTitle LIKE '%斯里兰卡%'",
    "UPDATE sycm_item_trend SET package_name='美加' WHERE itemTitle LIKE '%美加%' \
OR itemTitle LIKE '%美国%' \
OR itemTitle LIKE '%关岛%' \
OR itemTitle LIKE '%塞班%' \
OR itemTitle LIKE '%加拿大%'",
#     "UPDATE sycm_item_trend SET package_name='关岛塞班' WHERE itemTitle LIKE '%关岛%' \
# OR itemTitle LIKE '%塞班%'",
    "UPDATE sycm_item_trend SET package_name='俄罗斯' WHERE itemTitle LIKE '%俄罗斯%'"
]

'''
GTBU根据商品标题，进行套餐分组
分组规则内定，调整需跟陈友兴确认
'''
class PackageGroup(object):

    def __init__(self):
        self._db = pymysql.connect(config.DB_HOST, config.DB_USER, config.DB_PWD, config.DB_NAME,charset=config.DB_CHARSET)
        self._cursor = self._db.cursor()

    def executeSQL(self, sql):
        self._cursor.execute(sql)
        self._db.commit()

    def group(self):
        try:
            for sql in sycm_package_list_sql:
                self.executeSQL(sql)
        except Exception as e:
            print("Error: %s" % e)
        self._cursor.close()
        self._db.close()

if __name__ == '__main__':
    group = PackageGroup()
    group.group()
