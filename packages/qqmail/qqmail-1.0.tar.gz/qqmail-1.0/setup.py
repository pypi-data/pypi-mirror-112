# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='qqmail',# 需要打包的名字,即本模块要发布的名字
    version='v1.0',#版本
    description='Send your mail ordinary!', # 简要描述
    py_modules=['qqmail.qqmail'],   #  需要打包的模块
    author='DY_XiaoDong', # 作者名
    packages=['qqmail'],
    author_email='xiaodong@indouyin.cn',   # 作者邮件
    url='', # 项目地址,一般是代码托管的网站
    requires=['smtplib'], # 依赖包,如果没有,可以不要
    install_requires=[], # 强制下载的依赖包
    license='MIT',
)
