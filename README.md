# GTBU 数据爬取脚本

本脚本用于支撑GTBU竞争对手数据分析，数据来自携程、生意参谋、飞猪商城。

注意：

以下所有数据被保存到了 MySQL 数据库，数据库信息如下：

- 连接地址：10.1.210.50:3306
- 库名： market
- 用户密码：jiang/jiang

## 目录说明
crawler：    
    crontab 脚本，已使用 crontab 定时在 10.1.210.50 系统定时执行，
     
sycm：   
    生意参谋数据爬取脚本，需手动执行。

## 操作维护

### crawler

1. 已在 10.1.210.50 服务器上定时执行，服务器用户密码：root/123456
2. 脚本路径： /opt/crawler/gt_crawler_bak
3. 定时时间：  

        0 8 * * * root /opt/crawler/gt_crawler_bak/ctrip.sh
        0 8 * * * root /opt/crawler/gt_crawler_bak/fliggy.sh
        0 9,10,11 * * * root /opt/crawler/gt_crawler_bak/package.sh
        0 12 * * 0 root /opt/crawler/gt_crawler_bak/sunday_cron.sh
4. 如需调整，本地调试完，更新到服务器上去。

## sycm

1. 程序入口类：Application
2. 执行时间：每周一执行

执行操作流程：  

1. 登录生意参谋主页: https://sycm.taobao.com/custom/login.htm
2. 打开调试，复制 cookie 和 referer 到 Config.py，替换原有变量 （到此可完成程序登录认证）
3. 设置 Application main 方法中 saturday_date 为上周六的日期，例如：  
        saturday_date = Common.get_date_time('2018-09-15')
4. 运行程序

检查数据是否完整：  

SELECT cmDate, COUNT(1) FROM sycm_hot_sale_produce GROUP BY cmDate ORDER BY cmDate DESC;  
-- 每天的数据都是 500 条  

-- 需修改时间段为上上周日到上周六  
SELECT COUNT(DISTINCT itemId) FROM sycm_hot_sale_produce WHERE cmDate BETWEEN '2018-09-09' AND '2018-09-15';  
-- 总商品数量  
SELECT cmDate, COUNT(1) FROM sycm_item_trend GROUP BY cmDate ORDER BY cmDate DESC;  
-- 每天的数据量与上周总商品数据量相同

-- 检查套餐分组是否完成  
SELECT DISTINCT itemTitle, package_name FROM sycm_item_trend WHERE package_name IS NULL OR package_name = '';  
-- 若结果集不为空，存在未分组套餐，需要根据商品标题分组。分组规则咨询陈友兴。

如需套餐分组，修改 PackageGroup 中的 SQL，执行之。  

