#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019/4/4  15:11 
# @Author  : Andrew
# @File    : packageReturnReason
import json
import requests

FEDEX_URL = "https://www.fedex.com/trackingCal/track"

QUERY_PARAMETER = {
    "data": "{\"TrackPackagesRequest\":{\"appType\":\"WTRK\",\"appDeviceType\":\"DESKTOP\",\"supportHTML\":true,\"supportCurrentLocation\":true,\"uniqueKey\":\"\",\"processingParameters\":{},\"trackingInfoList\":[{\"trackNumberInfo\":{\"trackingNumber\":\"74890983235134819120\",\"trackingQualifier\":\"\",\"trackingCarrier\":\"\"}}]}}",
    "action": "trackpackages",
    "locale": "en_US",
    "version": "1",
    "format": "json",
    "perPageCount": 10
}

FEDEX_HEADER = {
    'Accept': '*/*',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Connection': 'keep-alive',
    'Content-Length': '483',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'fdx_cbid=31214489081554275515233690319081; _abck=91DA2D9523DFA97B3C45BF04105AC8E2~0~YAAQFWgDF5O/KeFpAQAA3UMK4gGxwN+Lbbm5r1fsC2gr82haXiyFyNtGzwzEyCg9QjRPr0rrppJE+zmcNLWHGjo2xpFgTpd92oKmzso7fNGjguLWV1/uG3HpN4bTfn1pMVnsHjDTOj01AD7Hm4Y8QhnTE0YoiK56FWZ6t6YJpedsU4T9IPNbrVs2OTnDGWbuzDYcRqgoxBTcYz4JSu2ZYhzOYVPq+dSSDfqGmzjIcBz14n0LlsplanZ8vF5o/Z8aJsRc8x58TAVsoogiYsgzrs26u0C4zlMTnOzZJwf/v/snCVp0WfpITQ==~-1~-1~-1; wdpl_id=31214489081554275515233690319081_1554275519095; bm_sz=3632623ADD1812DBC0EE400FA2550978~YAAQROI+F3JuLeRpAQAA1akg5wOwXGm/0aKDswcGvHSfdWwX31onW1MC1LLVQuAYA5J0tIwtNeeMt6YJ1sl+lFH7SoccrkRN+2xwL/zrjScMVNhSW24CzkQ+UkSGMwe3V+Uk9qJH81H/ONYF8sIaNBH/MCbH8B4GPBdQJcphFqXGAesc/Rzej1MC5Mb/C/A=; ak_bmsc=2EB68114DB00025116D898D6AA4A4688173EE2448218000027AAA55C0B7CDD3A~plIhMPmVgg4X1dO9zF4wHkvxitp5RnOMKueTI4o8pyQ5rFvh8OY7ElYgPZ2zMevoSWDeJ+TgksBHOgmTk6MrOFlpA5i76imbXAhjhJ2qKw705AEaxtuxYeyvw11lDWsj6HO07WSv2cRFlcdVvoOkdn7SsekKc1/00ak6n0aGbcq1rTNRvw2RtvDcvF5F72BymfwOU5xdRoXBMvIZxNkO4iVpUQDiYN1D7o642jBwRtUkuPafbKC1pnBQsyLllHWsBP; AMCVS_1E22171B520E93BF0A490D44%40AdobeOrg=1; AMCV_1E22171B520E93BF0A490D44%40AdobeOrg=817868104%7CMCIDTS%7C17990%7CMCMID%7C75535802810508911620672006494902855241%7CMCAAMLH-1554880319%7C11%7CMCAAMB-1554965672%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1554368072s%7CNONE%7CMCAID%7CNONE; s_sq=%5B%5BB%5D%5D; fdx_locale=en_US; mbox=session#1554360872323-337127#1554362829; s_pers=%20s_vnum%3D1554393600882%2526vn%253D1%7C1554393600882%3B%20gpv_pageName%3Dus%252Fen%252Ffedex%252Funified%252Ftrackdetailspage%7C1554362762275%3B%20s_nr%3D1554360962278-Repeat%7C1585896962278%3B%20s_invisit%3Dtrue%7C1554362762281%3B%20s_tbm%3D1%7C1554362762283%3B%20s_dfa%3Dfedexus%252Cfedexglbl%7C1554362769177%3B; s_sess=%20s_cm%3DundefinedTyped%252FBookmarkedTyped%252FBookmarkedundefined%3B%20s_visit%3D1%3B%20SC_LINKS%3D%3B%20s_cpc%3D0%3B%20s_ppv%3Dus%252Fen%252Ffedex%252Funified%252Ftrackdetailspage%3B%20s_cc%3Dtrue%3B%20setLink%3D%3B; Nina-nina-fedex-session=%7B%22locale%22%3A%22en_us%22%2C%22lcstat%22%3Afalse%7D; tracking_locale=en_US; siteDC=edc; bm_sv=5C3273ADF0CA3D5B013D49E38A91C667~Sl0D+i+Gitv4AlUlDElZJb7VBF8GrINvGWunXNCswXiKC1nPK/Y6NNU7Jv6f1FV9MpGdMoWHiQyEFSR8ufmnHqidZFNOpkPUokixGkl1xhIzQcQLgrjMHkQmHtyDdxvQVMdYIEfOOf9ujQXUcMDpba90S0DtfWsu8UENponhNgQ=',
    'Host': 'www.fedex.com',
    'Origin': 'https://www.fedex.com',
    'Referer': 'https://www.fedex.com/apps/fedextrack/?action=track&tracknumbers=74890983235134819120&locale=en_US&cntry_code=us',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}


def fetch():
    result = requests.post(FEDEX_URL, data=QUERY_PARAMETER, headers=FEDEX_HEADER)
    result_json = json.loads(result.text)
    package_list = result_json["TrackPackagesResponse"]["packageList"]
    for package_info in package_list:
        event_list = package_info.get("scanEventList")
        for event in event_list:
            scan_details = event.get("scanDetails")
            details = scan_details.strip()
            if details is "" or len(details) == 0:
                continue
            print(details)


fetch()