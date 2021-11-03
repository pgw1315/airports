#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@文件        :test_chrome.py
@时间        :2021/11/03 10:09:51
@作者        :Will
@版本        :1.0
@说明        : 测试Chrome浏览器是否安装成功
'''



from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')    # 禁止沙箱模式，否则肯能会报错遇到chrome异常
url="https://www.west.cn/login.asp"
brower=webdriver.Chrome(executable_path="./chromedriver", chrome_options=chrome_options)
brower.get(url)
print(brower.current_url)
brower.get("https://www.west.cn/Manager/")
print(brower.current_url)
brower.quit()
