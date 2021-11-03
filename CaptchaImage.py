#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@文件        :CaptchaImage.py
@时间        :2021/10/30 23:27:23
@作者        :Will
@版本        :1.0
@说明        : 图片验证码破解
'''


from io import BytesIO
import re
import time
import platform
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random

from Utils import getCapImage, getGapPos, saveLinks, simulateDragX

class CaptchaImage(object):
    # 验证码图片在html中的路径
    capImgXpath = '/html/body/div[2]/div[2]/div[1]/div/div[1]/div[1]/div/a/div[1]/div'
    # 拖拽手柄xpath
    handleXpath = '/html/body/div[2]/div[2]/div[1]/div/div[1]/div[2]/div[2]'

    def __init__(self):
        self.chrome_options = Options()
        # 驱动所在的路径
        self.driver_path = "/root/airports/chromedriver"
        # 根据电脑不同加载不同配置
        sysstr = platform.system()
        if(sysstr == "Linux"):
            self.chrome_options.add_argument("--headless")
            self.chrome_options.add_argument('--disable-gpu')
            self.chrome_options.add_argument('--no-sandbox')    # 禁止沙箱模式，否则肯能会报错遇到chrome异常
            self.CAP_IMG_OFFSET_Y = -130
            self.LOAD_SLEEP_TIME = 10
        else:
            # 验证码偏移位置
            self.CAP_IMG_OFFSET_Y = 0
            # 等待页面加载时间
            self.LOAD_SLEEP_TIME=3

        # self.chrome_options.add_argument("--headless")
        # self.chrome_options.add_argument('--disable-gpu')
        # self.chrome_options.add_argument('--no-sandbox')    # 禁止沙箱模式，否则肯能会报错遇到chrome异常
        # url="https://www.reoen.top/auth/register"

        self.driver = webdriver.Chrome(
            executable_path=self.driver_path, chrome_options=self.chrome_options)
        self.driver.maximize_window()

 

    def sliderVerify(self):
        # 点击出现验证码
        self.driver.refresh()
        time.sleep(self.LOAD_SLEEP_TIME)
        curTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(curTime+'  页面加载完成开始验证。。。')
        enCap=self.driver.find_element_by_xpath(
            '//*[@id="embed-captcha"]')
        if enCap:
            enCap.click()
        else:
            print('页面没有完全加载，请调长页面加载时间！！')
            return False
        time.sleep(2)
        # 隐藏缺口
        self.driver.execute_script(
            "document.getElementsByClassName('geetest_canvas_fullbg')[0].style.display='block';")
        time.sleep(1)
        # 获取没有缺口的验证码图片
        capImg1 = getCapImage(self.driver,self.capImgXpath,self.CAP_IMG_OFFSET_Y,'cap01.png')
        # 显示缺口
        self.driver.execute_script(
            "document.getElementsByClassName('geetest_canvas_fullbg')[0].style.display='none';")
        time.sleep(1)
        # 获取没有缺口的验证码图片
        capImg2 = getCapImage(self.driver,self.capImgXpath,self.CAP_IMG_OFFSET_Y,'cap02.png')
        # 获取的缺口的位置
        # gapPos = self.getGapPos(capImg1, capImg2)
        gapPos = getGapPos(capImg1, capImg2)
        # 获取到当前时间
        curTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(curTime+'  图片缺口的位置：', gapPos)
        if not gapPos or gapPos <= 50:
            return False

        gapPos -= 2
        handle = self.driver.find_element_by_xpath(self.handleXpath)
        simulateDragX(self.driver,handle, gapPos)
        time.sleep(1)
        # 判断是否验证成功
        stag = self.driver.find_element_by_css_selector(
            ".geetest_success_radar_tip_content")
        if stag.size['width'] > 0:
            curTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(curTime+'  验证成功！开始注册。。。')
            return True
        else:
            curTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(curTime+'  验证失败！')
            return False
    # 开始验证

    def start(self, url,path):
        self.driver.get(url)
        curTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(curTime+'  打开网址:', url)
        time.sleep(2)
        success=False
        # 验证成功
        while not success:
            success=self.sliderVerify()
        # 图片验证码验证成功
        # 随机字符串
        randomStr = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789', 10))
        # 注册邮箱
        email = randomStr + '@gmail.com'
        # 注册
        self.driver.find_element_by_css_selector("#name").send_keys(randomStr)
        self.driver.find_element_by_css_selector("#email").send_keys(randomStr)
        self.driver.find_element_by_css_selector("#passwd").send_keys(randomStr)
        self.driver.find_element_by_css_selector("#repasswd").send_keys(randomStr)
        time.sleep(2)
        self.driver.find_element_by_css_selector("#register-confirm").click()
        time.sleep(5)
        try:
            # 点击注册完成
           self.driver.find_element_by_xpath('/html/body/div[3]/div/div[3]/button[1]').click()
           curTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
           print(curTime+'  注册成功：',randomStr)
           time.sleep(self.LOAD_SLEEP_TIME)
           # 点击签到
           self.driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/section/div[1]/div/div/a').click()
           curTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
           print(curTime+'  签到完成！')
           html = self.driver.execute_script("return document.documentElement.outerHTML")
           saveLinks(html,path)
           curTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
           print(curTime+'  订阅链接保存完成')
        except Exception as e:
           print('注册失败')

           print(e)
           self.driver.quit()
           pass
        
        


    def close(self):
        # 关闭浏览器
        self.driver.quit()
