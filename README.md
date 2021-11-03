# 自动注册

## 安装 
### 安装python3
#### 配epel源_阿里
```bash
wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo
```
#### 安装python3
```bash
yum install python36 -y 
```

### 安装扩展库
```bash
pip3 install requests
```
### 安装Chrome
首先安装google的epel源
```bash 
vi /etc/yum.repos.d/google.repo
```
```python 
[google]
name=Google-x86_64
baseurl=http://dl.google.com/linux/rpm/stable/x86_64
enabled=1
gpgcheck=0
gpgkey=https://dl-ssl.google.com/linux/linux_signing_key.pub 
```
安装Chrome
```python 
yum update && yum install google-chrome-stable
```
### 下载驱动
https://npm.taobao.org/mirrors/chromedriver/

找到chrome对应的chromedriver 版本，并下载
```bash 
wget https://chromedriver.storage.googleapis.com/74.0.3729.6/chromedriver_linux64.zip
```

**将下载的chromedriver 放到脚本同级目录调用** 

### 为chromedriver授权
```bash 
chmod 755 chromedriver
```


## 配置计划任务
```bash
vim /etc/crontab
```
```bash

ROOT_PATH=/root/airports/

5 * * * * root PYTHONIOENCODING=utf-8 /usr/bin/python3 $ROOT_PATH/refresh.py >> $ROOT_PATH/logs/refresh.log 2>&1
1 */5 * * * root PYTHONIOENCODING=utf-8 /usr/bin/python3 $ROOT_PATH/main.py >> $ROOT_PATH/logs/reg.log 2>&1
```