#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/28 11:14 
# @Author  : shuzf
# @File    : setup.py

import setuptools

with open("README.md", "r",encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="jsonpath_expression",
    version="0.3",
    author="shuzhifu",
    author_email="ishuzf@163.com",
    description="jsonpath expression generate",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/ishuzf/jsonpath_expression",
    packages=setuptools.find_packages(),
    install_requires=['jsonpath>=0.82'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)