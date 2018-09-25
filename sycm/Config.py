# -*- coding: UTF-8 -*-
'''
@author: Andrewzhj
@contact: andrew_zhj@126.com
@file: Config.py
@time: 2018/8/30 18:08
@desc:
@note:
'''

HEADER = {
    "accept": "*/*",
    # "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "cookie": "miid=521382484800308255; cna=wUEPEj19GQ8CATr7Jc0+bmHf; enc=xkpks22MdCE9fhiGLKQbqX3nBwQZ%2BpO9tJb54ReT4%2F8%2FWuBTPz0rfMh3Dn9DM5NlvxIG4m%2BbqyDN3gcLAM7KSQ%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; t=581cb19d0f97f71e8b9ea8c52c8a5c9c; uc3=id2=&nk2=&lg2=; tracknick=; JSESSIONID=0F216D0E402AB48173689C898D9A6A35; cookie2=18882167a283322cf4630c710c32c6cb; _tb_token_=e09e8e381e7ed; x=2602163414; uc1=cookie14=UoTfLQuLObf7DA%3D%3D&lng=zh_CN; skt=435a464a21d0a8c7; sn=%E6%B7%B1%E5%9C%B3%E4%BC%98%E5%85%8B%E8%81%94%E6%97%85%E6%B8%B8%E4%B8%93%E8%90%A5%E5%BA%97%3A%E6%95%B0%E6%8D%AE8; unb=4103374153; csg=f84b05c3; _euacm_ac_l_uid_=4103374153; 4103374153_euacm_ac_c_uid_=2602163414; 4103374153_euacm_ac_rs_uid_=2602163414; _euacm_ac_rs_sid_=129049361; v=0; _portal_version_=new; mkt_gray=1; isg=BOfnyXCjcGQdE_WGRu0xPFZ3dhu7bYnf2L5Ho7lUA3adqAdqwTxLniWuzuiTW5PG",
    "referer": "https://sycm.taobao.com/mq/industry/property/property.htm?spm=a21ag.7782695.LeftMenu.d331.2d3e46535WYsV2",
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
}

LOGIN_USER = {
    'act': 'login',
    'TPL_username': '***',
    'TPL_password': '***'
}

''' MySQL Config  '''
DB_HOST = '10.1.210.50'
DB_USER = 'jiang'
DB_PWD = 'jiang'
DB_NAME = 'market'
DB_CHARSET = 'utf8'