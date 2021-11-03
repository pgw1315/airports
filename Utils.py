#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@文件        :Utils.py
@时间        :2021/10/31 02:33:54
@作者        :Will
@版本        :1.0
@说明        :
'''
# 获取验证码图片
from io import BytesIO
import json
import re
import time
import random
from PIL import Image
from selenium import webdriver

def saveLinks(html,path):
    subLinks={}
    # shadowrocket客户端
    tags = re.finditer(r'https?://.*?/link/.*\?\w+=shadowrocket', html)
    for tag in tags:
        subLinks['shadowrocket'] = tag.group()
    # Clash客户端
    tags = re.finditer(r'https?://.*?/link/.*\?clash=\w+', html)
    for tag in tags:
        subLinks['clash'] = tag.group()
    # V2ray客户端
    tags = re.finditer(r'https?://.*?/link/.*\?sub=3+', html)
    for tag in tags:
        subLinks['v2ray'] = tag.group()
    print(subLinks)
    # 保存订阅链接
    jLinks=json.dumps(subLinks)
    with open(path+'links','w',encoding='utf-8') as f:
        f.write(jLinks)

def __getRadomPauseScondes():
    """
    :return:随机的拖动暂停时间
    """
    return random.uniform(0.6, 0.9)

def simulateDragX(dirver, source, targetOffsetX):
    """
    模仿人的拖拽动作：快速沿着X轴拖动（存在误差），再暂停，然后修正误差
    防止被检测为机器人，出现“图片被怪物吃掉了”等验证失败的情况
    :param source:要拖拽的html元素
    :param targetOffsetX: 拖拽目标x轴距离
    :return: None
    """
    action_chains = webdriver.ActionChains(dirver)
    # 点击，准备拖拽
    action_chains.click_and_hold(source)
    # 拖动次数，二到三次
    dragCount = random.randint(2, 3)
    if dragCount == 2:
        # 总误差值
        sumOffsetx = random.randint(-15, 15)
        action_chains.move_by_offset(targetOffsetX + sumOffsetx, 0)
        # 暂停一会
        action_chains.pause(__getRadomPauseScondes())
        # 修正误差，防止被检测为机器人，出现图片被怪物吃掉了等验证失败的情况
        action_chains.move_by_offset(-sumOffsetx, 0)
    elif dragCount == 3:
        # 总误差值
        sumOffsetx = random.randint(-15, 15)
        action_chains.move_by_offset(targetOffsetX + sumOffsetx, 0)
        # 暂停一会
        action_chains.pause(__getRadomPauseScondes())

        # 已修正误差的和
        fixedOffsetX = 0
        # 第一次修正误差
        if sumOffsetx < 0:
            offsetx = random.randint(sumOffsetx, 0)
        else:
            offsetx = random.randint(0, sumOffsetx)

        fixedOffsetX = fixedOffsetX + offsetx
        action_chains.move_by_offset(-offsetx, 0)
        action_chains.pause(__getRadomPauseScondes())

        # 最后一次修正误差
        action_chains.move_by_offset(-sumOffsetx + fixedOffsetX, 0)
        action_chains.pause(__getRadomPauseScondes())

    else:
        raise Exception("莫不是系统出现了问题？!")

    # 参考action_chains.drag_and_drop_by_offset()
    action_chains.release()
    action_chains.perform()

def getCapImage(driver,xpath,offsetY, fileName='cap.png'):
    img = driver.find_element_by_xpath(xpath)
    time.sleep(0.5)
    location = img.location
    size = img.size
    # 图片的偏移量
    
    top, bottom, left, right = location['y']+offsetY, location['y'] + \
        size['height']+offsetY, location['x'], location['x']+size['width']
    screenshot = driver.get_screenshot_as_png()
    screenshot = Image.open(BytesIO(screenshot))
    captcha = screenshot.crop((left, top, right, bottom))
    captcha.save(fileName)
    return captcha
    
   # 获取缺口的位置
def getGapPos( img1, img2, left=50):
    # 定义像素差值的大小
    gap = 20
    # 将图片转换为黑白图片
    img1 = img1.convert("L")
    img2 = img2.convert("L")
    # 获取到图片的宽和高
    size = img1.size

    width = size[0]
    height = size[1]
    # print('验证图片宽：  高：', width, height)
    # 遍历所有的像素
    for x in range(left, width):
        for y in range(height):
            # 得到每个像素的值
            pixel1 = img1.load()[x, y]
            pixel2 = img2.load()[x, y]
            # 判断像素之间的差别
            pixelGap = abs(pixel1-pixel2)
            # 如果像素之间的差值大于设定值直接返回
            if pixelGap >= gap:
                return x