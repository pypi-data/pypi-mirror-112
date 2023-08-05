# -*- coding: utf-8 -*-
# @Time    : 2021/7/6 5:56 下午
# @Author  : X.Lin
# @Email   : ****
# @File    : setup.py
# @Software: PyCharm
# @Desc    :

import setuptools

setuptools.setup(
    name="mx_helpers",  # Replace with your own username  #自定义封装模块名与文件夹名相同
    version="0.0.1",  # 版本号，下次修改后再提交的话只需要修改当前的版本号就可以了
    author="MiXian",  # 作者
    author_email="xlin0721@163.com",  # 邮箱
    description="封装自用帮助库",  # 描述
    long_description='封装自用帮助库',  # 描述
    long_description_content_type="text/markdown",  # markdown
    # url="https://github.com/tanxinyue/multable",  # github地址
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # License
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # 支持python版本
)
