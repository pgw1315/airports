#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 作者:will
# 创建时间:2021/10/24 4:09 下午
# 文件名： Airport
# 开发软件: PyCharm
# 添加
import random
import requests
import json
import re
import os
class Airport(object):
    subLinks = {}
    


    def __init__(self, host,path,prefix=''):
        # 判断文件夹是否存在
        if  not os.path.isdir(path) :
            os.makedirs(path)
        self.path=path
        # 订阅链接前缀
        self.prefix=prefix
        self.session = requests.Session()
        # 注册地址
        self.regUrl = host + '/auth/register'
        # 登陆地址
        self.loginUrl = host + '/auth/login'
        # 签到链接
        self.checkinUrl = host + '/user/checkin'
        # 用户中心地址
        self.userUrl = host + '/user'

        # 随机字符串
        self.randomStr = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789-', 10))
        # 注册邮箱
        self.email = self.randomStr + '@gmail.com'

        self.header = {
            'authority': host,
            'sec-ch-ua': 'Microsoft Edge;v=93,  Not;A Brand;v=99, Chromium;v=93',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'x-requested-with': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 Edg/93.0.961.52',
            'sec-ch-ua-platform': 'macOS',
            'origin': host,
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': host,
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'cookie': 'lang=zh-cn'
        }

    def registered(self):
        print('开始注册......')
        # 注册信息
        regData = {
            'email': self.email,
            'name': self.randomStr,
            'passwd': self.randomStr,
            'repasswd': self.randomStr,
            'code': 0
        }
        response = self.session.post(url=self.regUrl, params=regData, headers=self.header)
        if response.status_code == 200:
            content = response.text
            if content:
                try:
                    content = content.encode('utf-8').decode('unicode_escape')
                except Exception as e:
                    pass
            msg = json.loads(content)
            if msg['ret'] == 1:
                print('注册成功')
                print('用户名:'+self.email)
                print('密码:'+self.randomStr)

                return True
            else:
                return False

    def login(self):
        # 注册成功，登陆
        loginData = {
            'email': self.email,
            'passwd': self.randomStr,
            'code': ''
        }
        loginRes = self.session.post(self.loginUrl, params=loginData, headers=self.header)
        loginRes = loginRes.text.encode('utf-8').decode('unicode_escape')
        loginMsg = json.loads(loginRes)
        if loginMsg['ret'] == 1:
            self.session.post(self.checkinUrl)
            return True
        else:
            return False

    def forLink(self):
        # 获取链接
        userRes = self.session.get(self.userUrl)
        html = userRes.text
        # shadowrocket客户端
        tags = re.finditer(r'https?://.*?/link/.*\?\w+=shadowrocket', html)
        for tag in tags:
            self.subLinks['shadowrocket'] = tag.group()
        # Clash客户端
        tags = re.finditer(r'https?://.*?/link/.*\?clash=\w+', html)
        for tag in tags:
            self.subLinks['clash'] = tag.group()
        # V2ray客户端
        tags = re.finditer(r'https?://.*?/link/.*\?sub=3+', html)
        for tag in tags:
            self.subLinks['v2ray'] = tag.group()
        return self.subLinks

    def saveLinks(self):
        airportPath=self.path + self.prefix
        # 保存订阅链接
        jLinks=json.dumps(self.subLinks)
        with open(airportPath+'links','w',encoding='utf-8') as f:
            f.write(jLinks)

        


