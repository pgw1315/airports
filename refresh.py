#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@文件        :refresh.py
@说明        :
@时间        :2021/10/24 20:33:52
@作者        :Will
@版本        :1.0
'''

import  os
import  json
import requests
import base64
import urllib 
import re
import time

# 订阅链接所在的目录
SUB_PATH = '/root/airports/sub/'
LINK_PATH = '/root/airports/links/'

# SUB_PATH = './sub/'
# LINK_PATH = './links/'
# 订阅链接的前缀

links=None

def refresh(linkFile,prefix):
    # 读取订阅链接文件
    try:
        with open(linkFile) as f:
            content = f.readline()
            links=json.loads(content)
    except Exception as e:
        print(e)
        print('链接文件找不到，打开文件失败！')


    if links :
        # 下载订阅文件
        for name,link in links.items():
            fileName=prefix+name
            filePath=SUB_PATH+ fileName
            r = requests.get(link) 
            with open(filePath, "w",encoding='utf-8') as f:
                content=r.text
                # 对文件内容进行处理
                if fileName == 'uu_clash':
                    content=re.sub(r'Rule:','rules:',content)

                # print(r.text)
                f.write(content)
if __name__ == '__main__':
    
    # 判断文件夹是否存在
    if  not os.path.isdir(SUB_PATH) :
        os.makedirs(SUB_PATH)
    if  not os.path.isdir(SUB_PATH) :
        os.makedirs(SUB_PATH)
    print( '********************************'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'********************************')

    refresh(LINK_PATH+'uu_links','uu_')
    print('updated uu_links success ')
    refresh(LINK_PATH+'nn_links','nn_')
    print('updated nn_links success ')
    refresh(LINK_PATH+'jj_links','jj_')
    print('updated jj_links success ')