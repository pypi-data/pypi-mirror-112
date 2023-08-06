# -*- coding: utf-8 -*- 
# @Time : 2021/7/9 下午5:39 
# @Author : Jianglin Zhang 
# @File : setup.py

from setuptools import setup, find_packages

setup(
    name="ws_common",
    version="1.0.0",
    author="Jianglin Zhang",
    author_email="jianglin.zhang@westwell-lab.com",
    description="ws common",
    # 项目主页
    url="http://www.westwell-lab.com/",
    # 你要安装的包，通过 setuptools.find_packages 找到当前目录下有哪些包
    # classifiers=[
    #     'Development Status :: 1.0.0-Alpha',
    #
    #     # 开发的目标用户
    #     'Intended Audience :: Developers',
    #
    #     # 属于什么类型
    #     'Topic :: Software Development :: Common Tools',
    #
    #     # 许可证信息
    #     'License :: OSI Approved :: GPL License',
    #
    #     # 目标 Python 版本
    #     'Programming Language :: Python :: 3.6',
    #     'Programming Language :: Python :: 3.7',
    # ],
    packages=find_packages(),

    data_files=[
        #('./', ['config/*.ini']),
        #('/home/wwl/mypython/myworkspace/test/video/', ['*.avi']),
    ],

    # 希望被打包的文件
    # package_data={
    #     '': ['*.ini'],
    #     'config': ['*.ini']
    # },
    # 不打包某些文件
    exclude_package_data={
        './logs': ['*.log']
    },
    install_requires=['opencv-python', ],
    setup_requires=['pbr'],
)
