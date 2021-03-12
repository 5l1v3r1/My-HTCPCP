#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
中金所股指期货分析utils
测试数据：http://www.cffex.com.cn/lssjxz/
'''

import csv
import os


import os
import csv

buy = ['6206']
sale = []
start = "201712"
for path in os.listdir('.'):
    if path=="." or path==".." or path==start:
        continue
    if os.path.isdir(path):
        date_str = path[-4:]
        csv_list = []
        for csv_file in os.listdir(path):
            csv_list.append(csv_file)
        target_csv = csv_list[-2]
        with open(f"{path}/{target_csv}", "rb") as sd:
            r = csv.DictReader(sd)   #为每行创建一个字典，同时将字段名称与表头对应
            for line in r:
                if line["合约代码"]==f"IC{date_str}":
                    sss.append(line['今收盘'])
        


'''
判定结算日
由于判定是否是交易日非常麻烦，
所以直接从数据的日期里找，
目前期货结算日规定：
合约到期月份的第三个周五，遇法定节假日顺延。
'''
def check_settle_day():
    pass