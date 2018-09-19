# -*- coding: UTF-8 -*-
'''
@author: Andrewzhj
@contact: andrew_zhj@126.com
@file: package_group.py
@time: 2018/8/22 11:07
@desc:
@note:
'''
import pymysql
db = pymysql.connect("10.1.210.50", "jiang", "jiang", "market", charset='utf8')
cursor = db.cursor()

'''
套餐分组语句
'''
# 标记携程套餐组 SQL
ctrip_package_sql_list = [
    "UPDATE ctrip_wifi SET package_name='全球' WHERE title LIKE '马尔代夫%' OR title LIKE '全球%' OR title LIKE '毛里求斯%' \
    OR title LIKE '斯里兰卡%' OR title LIKE '印度%' OR title LIKE '摩洛哥%' OR title LIKE '阿联酋%' OR title LIKE '突尼斯%' \
    OR title LIKE '埃及%' OR title LIKE '中东非%' OR title LIKE '南非%' OR title LIKE '以色列%' OR title LIKE '亚洲%' \
    OR title LIKE '斐济%' OR title LIKE '巴西%' OR title LIKE '尼泊尔%' OR title LIKE '非洲%' \
    OR title LIKE '阿根廷%' OR title LIKE '伊拉克%' OR title LIKE '阿曼%' OR title LIKE '中南美%'",
    "UPDATE ctrip_wifi SET package_name='欧洲' WHERE  title LIKE '欧洲%'",
    "UPDATE ctrip_wifi SET package_name='日本' WHERE title LIKE '日本%' OR title LIKE '日韩%'",
    "UPDATE ctrip_wifi SET package_name='韩国' WHERE title LIKE '%韩国%'",
    "UPDATE ctrip_wifi SET package_name='俄罗斯' WHERE title LIKE '%俄罗斯%'",
    "UPDATE ctrip_wifi SET package_name='台湾' WHERE title LIKE '%台湾%'",
    "UPDATE ctrip_wifi SET package_name='泰国' WHERE title LIKE '%泰国%'",
    "UPDATE ctrip_wifi SET package_name='东南亚' WHERE  title LIKE '东南亚%' \
    OR title LIKE '越南%' OR title LIKE '马来西亚%' OR title LIKE '新加坡%' OR title LIKE '柬埔寨%' \
    OR title LIKE '菲律宾%' OR title LIKE '巴厘岛%' OR title LIKE '印尼%' OR title LIKE '新马泰%' \
    OR title LIKE '文莱%' OR title LIKE '老挝%' OR title LIKE '缅甸%'",
    "UPDATE ctrip_wifi SET package_name='港澳' WHERE  title LIKE '香港%' OR title LIKE '港澳%' OR title LIKE '澳门%'",
    "UPDATE ctrip_wifi SET package_name='澳新' WHERE  title LIKE '澳新%' OR title LIKE '新西兰%' OR title LIKE '澳大利亚%'",
    "UPDATE ctrip_wifi SET package_name='关岛塞班' WHERE  title LIKE '关岛塞班%' OR title LIKE '塞班%'",
    "UPDATE ctrip_wifi SET package_name='北美三国' WHERE  title LIKE '美国%' OR title LIKE '加拿大%' OR title LIKE '美加%' \
    OR title LIKE '北美三国%' OR title LIKE '%美国WiFi%'"
]

ctrip_sunday_package_sql_list = [
    "UPDATE ctrip_sunday_wifi SET package_name='全球' WHERE title LIKE '马尔代夫%' OR title LIKE '全球%' OR title LIKE '毛里求斯%' \
    OR title LIKE '斯里兰卡%' OR title LIKE '印度%' OR title LIKE '摩洛哥%' OR title LIKE '阿联酋%' OR title LIKE '突尼斯%' \
    OR title LIKE '埃及%' OR title LIKE '中东非%' OR title LIKE '南非%' OR title LIKE '以色列%' OR title LIKE '亚洲%' \
    OR title LIKE '斐济%' OR title LIKE '巴西%' OR title LIKE '尼泊尔%' OR title LIKE '非洲%' \
    OR title LIKE '阿根廷%' OR title LIKE '伊拉克%' OR title LIKE '阿曼%' OR title LIKE '中南美%'",
    "UPDATE ctrip_sunday_wifi SET package_name='欧洲' WHERE  title LIKE '欧洲%'",
    "UPDATE ctrip_sunday_wifi SET package_name='日本' WHERE title LIKE '日本%' OR title LIKE '日韩%'",
    "UPDATE ctrip_sunday_wifi SET package_name='韩国' WHERE title LIKE '%韩国%'",
    "UPDATE ctrip_sunday_wifi SET package_name='俄罗斯' WHERE title LIKE '%俄罗斯%'",
    "UPDATE ctrip_sunday_wifi SET package_name='台湾' WHERE title LIKE '%台湾%'",
    "UPDATE ctrip_sunday_wifi SET package_name='泰国' WHERE title LIKE '%泰国%'",
    "UPDATE ctrip_sunday_wifi SET package_name='东南亚' WHERE  title LIKE '东南亚%' \
    OR title LIKE '越南%' OR title LIKE '马来西亚%' OR title LIKE '新加坡%' OR title LIKE '柬埔寨%' \
    OR title LIKE '菲律宾%' OR title LIKE '巴厘岛%' OR title LIKE '印尼%' OR title LIKE '新马泰%' \
    OR title LIKE '文莱%' OR title LIKE '老挝%' OR title LIKE '缅甸%'",
    "UPDATE ctrip_sunday_wifi SET package_name='港澳' WHERE  title LIKE '香港%' OR title LIKE '港澳%' OR title LIKE '澳门%'",
    "UPDATE ctrip_sunday_wifi SET package_name='澳新' WHERE  title LIKE '澳新%' OR title LIKE '新西兰%' OR title LIKE '澳大利亚%'",
    "UPDATE ctrip_sunday_wifi SET package_name='关岛塞班' WHERE  title LIKE '关岛塞班%' OR title LIKE '塞班%'",
    "UPDATE ctrip_sunday_wifi SET package_name='北美三国' WHERE  title LIKE '美国%' OR title LIKE '加拿大%' OR title LIKE '美加%' \
    OR title LIKE '北美三国%' OR title LIKE '%美国WiFi%'"
]

# 标记携程wifi覆盖国家归属
ctrip_country_sql_list = [
    "UPDATE ctrip_wifi SET country_id='1', country_name='全球' WHERE country_id IS NULL AND title LIKE '全球%' OR package_name='其他'",
    "UPDATE ctrip_wifi SET country_id='2', country_name='北美三国' WHERE country_id IS NULL AND title LIKE '北美三国%' OR title LIKE '美国%' OR package_name='北美三国'",
    "UPDATE ctrip_wifi SET country_id='3', country_name='东南亚' WHERE country_id IS NULL AND title LIKE '东南亚%' OR package_name='东南亚'",
    "UPDATE ctrip_wifi SET country_id='4', country_name='港澳' WHERE country_id IS NULL AND title LIKE '港澳%' OR package_name='港澳'",
    "UPDATE ctrip_wifi SET country_id='5', country_name='韩国' WHERE country_id IS NULL AND title LIKE '韩国%'",
    "UPDATE ctrip_wifi SET country_id='6', country_name='泰国' WHERE country_id IS NULL AND title LIKE '泰国%'",
    "UPDATE ctrip_wifi SET country_id='7', country_name='日本' WHERE country_id IS NULL AND title LIKE '日本%' OR title LIKE '日韩%'",
    "UPDATE ctrip_wifi SET country_id='8', country_name='台湾' WHERE country_id IS NULL AND title LIKE '%台湾%'",
    "UPDATE ctrip_wifi SET country_id='9', country_name='欧洲' WHERE country_id IS NULL AND title LIKE '欧洲%' OR package_name='欧洲'",
    "UPDATE ctrip_wifi SET country_id='10', country_name='澳新' WHERE country_id IS NULL AND title LIKE '澳新%' OR package_name='澳新'",
    "UPDATE ctrip_wifi SET country_id='11', country_name='俄罗斯' WHERE country_id IS NULL AND title LIKE '俄罗斯%'",
    "UPDATE ctrip_wifi SET country_id='12', country_name='关塞' WHERE country_id IS NULL AND title LIKE '关塞%' OR package_name='关岛塞班'"
]

fliggy_package_sql_list = [
    "UPDATE fliggy_wifi SET package_group='9', package_group_name='日本' WHERE  package_group IS NULL AND package_name LIKE '日本%' OR country='日本' OR package_name LIKE '%日本%'",
    "UPDATE fliggy_wifi SET package_group='10', package_group_name='欧洲' WHERE package_group IS NULL AND package_name LIKE '欧洲%' \
OR country='欧洲' \
OR package_name LIKE '%俄罗斯%' \
OR package_name LIKE '%英国%' \
OR package_name LIKE '%欧洲%' \
OR package_name LIKE '%法国%' \
OR package_name LIKE '%瑞士%' \
OR package_name LIKE '%土耳其%' \
OR package_name LIKE '%西班牙%' \
OR package_name LIKE '%捷克%' \
OR package_name LIKE '%希腊%' \
OR package_name LIKE '%芬兰%' \
OR package_name LIKE '%瑞典%' \
OR package_name LIKE '%冰岛%' \
OR package_name LIKE '%荷兰%' \
OR package_name LIKE '%匈牙利%' \
OR package_name LIKE '%挪威%' \
OR package_name LIKE '%奥地利%' \
OR package_name LIKE '%意大利%' \
OR package_name LIKE '%葡萄牙%' \
OR package_name LIKE '%德国%' \
OR package_name LIKE '%丹麦%' \
OR package_name LIKE '%克罗地亚%' \
OR package_name LIKE '%爱尔兰%' \
OR package_name LIKE '%罗马尼亚%' \
OR package_name LIKE '%波兰%' \
OR package_name LIKE '%乌克兰%' \
OR package_name LIKE '%立陶宛%' \
OR package_name LIKE '%马耳他%' \
OR package_name LIKE '%斯洛伐克%'",
    "UPDATE fliggy_wifi SET package_group='11', package_group_name='中港澳' WHERE package_group IS NULL AND package_name LIKE '中港澳%' \
OR country='中港澳' \
OR package_name LIKE '%香港%' \
OR package_name LIKE '%澳门%'",
    "UPDATE fliggy_wifi SET package_group='12', package_group_name='韩国' WHERE package_group IS NULL AND package_name LIKE '韩国%' \
OR country='韩国' \
OR package_name LIKE '%韩国%'",
    "UPDATE fliggy_wifi SET package_group='13', package_group_name='东南亚' WHERE package_name LIKE '东南亚%' \
OR country='东南亚' \
OR package_name LIKE '%新加坡%' \
OR package_name LIKE '%越南%' \
OR package_name LIKE '%菲律宾%' \
OR package_name LIKE '%印尼%' \
OR package_name LIKE '%马来西亚%' \
OR package_name LIKE '%柬埔寨%' \
OR package_name LIKE '%缅甸%'",
    "UPDATE fliggy_wifi SET package_group='15', package_group_name='泰国' WHERE package_group IS NULL AND package_name LIKE '泰国%' OR country='泰国'",
    "UPDATE fliggy_wifi SET package_group='16', package_group_name='美加' WHERE package_group IS NULL AND package_name LIKE '美加%' \
OR country='美加' \
OR package_name LIKE '%美国%' \
OR package_name LIKE '%关岛%' \
OR package_name LIKE '%加拿大%'",
    "UPDATE fliggy_wifi SET package_group='18', package_group_name='台湾' WHERE package_group IS NULL AND package_name LIKE '台湾%' OR country='台湾'",
    "UPDATE fliggy_wifi SET package_group='19', package_group_name='埃及阿联酋' WHERE package_group IS NULL AND package_name LIKE '埃及阿联酋%' \
OR country='埃及阿联酋' \
OR package_name LIKE '%阿联酋%' \
OR package_name LIKE '%埃及%'" ,
    "UPDATE fliggy_wifi SET package_group='20', package_group_name='澳新' WHERE package_group IS NULL AND package_name LIKE '澳新%' \
OR country='澳新' \
OR package_name LIKE '%澳大利亚%' \
OR package_name LIKE '%新西兰%'",
    "UPDATE fliggy_wifi SET package_group='21', package_group_name='其它' WHERE package_group IS NULL AND package_name LIKE '其它%' \
OR package_name LIKE '%马尔代夫%' \
OR package_name LIKE '%斯里兰卡%' \
OR package_name LIKE '%毛里求斯%' \
OR package_name LIKE '%南非%' \
OR package_name LIKE '%肯尼亚%' \
OR package_name LIKE '%哈萨克斯坦%' \
OR package_name LIKE '%巴西%' \
OR package_name LIKE '%印度%' \
OR package_name LIKE '%非洲%' \
OR package_name LIKE '%哥伦比亚%' \
OR package_name LIKE '%以色列%' \
OR package_name LIKE '%墨西哥%' \
OR package_name LIKE '%阿根廷%' \
OR package_name LIKE '%卡塔尔%' \
OR package_name LIKE '%全球%' \
OR package_name LIKE '%智利%' \
OR package_name LIKE '%哥斯达黎加%'"
]

ctrip_sale_rate_sql = [
    "DELETE FROM ctrip_main_line WHERE dateWeek=WEEK(NOW())-1",
    "INSERT INTO ctrip_main_line(title, producer, package_name,country_name, max_month_sale, max_total_money, dateWeek) \
    SELECT title, producer, package_name, country_name, MAX(month_sale) max_month_sale, \
    (MAX(month_sale) * MAX(price)) max_total_money, WEEK(fetch_date) dateWeek \
    FROM ctrip_wifi GROUP BY title, producer, dateWeek HAVING dateWeek=WEEK(NOW())-1",
    "DELETE FROM ctrip_main_line WHERE dateWeek=WEEK(NOW())",
    "INSERT INTO ctrip_main_line(title, producer, package_name,country_name, max_month_sale, max_total_money, dateWeek) \
    SELECT title, producer, package_name, country_name, MAX(month_sale) max_month_sale, \
    (MAX(month_sale) * MAX(price)) max_total_money, WEEK(fetch_date) dateWeek \
    FROM ctrip_wifi GROUP BY title, producer, dateWeek HAVING dateWeek=WEEK(NOW())",
]

def execut(sql_list):
    for sql in sql_list:
        cursor.execute(sql)
        db.commit()

def TagWifiProduce():
    try:
        execut(ctrip_package_sql_list)
        execut(ctrip_sunday_package_sql_list)
        execut(ctrip_country_sql_list)
        execut(fliggy_package_sql_list)
        execut(ctrip_sale_rate_sql)
    except Exception as e:
        print("error: %s" % e)
    finally:
        cursor.close()
        db.close()

if __name__ == '__main__':
    TagWifiProduce()