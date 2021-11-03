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

## 配置计划任务
```bash
vim /etc/crontab
```
```bash

ROOT_PATH=/root/airports/

5,20,35,50 * * * * root PYTHONIOENCODING=utf-8 /usr/bin/python3 $ROOT_PATH/refresh.py >> $ROOT_PATH/logs/refresh.log 2>&1
1,15,30,45 * * * * root PYTHONIOENCODING=utf-8 /usr/bin/python3 $ROOT_PATH/main.py >> $ROOT_PATH/logs/reg.log 2>&1
```