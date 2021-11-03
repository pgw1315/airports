#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 作者:will
# 创建时间:2021/10/24 4:17 下午
# 文件名： main


from Airport import Airport
import time

from CaptchaImage import CaptchaImage
SUB_PATH = '/root/airports/sub/'
LINK_PATH = '/root/airports/links/'
# LINK_PATH = './links/'
if __name__ == '__main__':
    print( '********************************'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'********************************')
    # UU机场
    uuAp=Airport('https://www.uuyun.one',LINK_PATH,prefix='uu_')
    if uuAp.registered():
        if uuAp.login():
            uuAp.forLink()
            uuAp.saveLinks()
    # 牛牛机场
    nnAp=Airport('https://xniuniu.xyz',LINK_PATH,prefix='nn_')
    if nnAp.registered():
        if nnAp.login():
            nnAp.forLink()
            nnAp.saveLinks()
    # 极简
    url="https://www.wiougong.fun/auth/register"
    ci=CaptchaImage()
    ci.start(url,LINK_PATH+'jj_')
    time.sleep(1)
    ci.close()

