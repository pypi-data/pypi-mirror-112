# -*- coding: utf-8 -*-
# @Time    : 2021/5/17 10:47 上午
# @Author  : X.Lin
# @Email   : ****
# @File    : __init__.py.py
# @Software: PyCharm
# @Desc    :
from mx_utils.logUtil import BaseLogs
logger = BaseLogs("mx_asyns").getLogging()
PROXY_STR = "http://127.0.0.1:7890"
# export https_proxy=http://127.0.0.1:7890 http_proxy=http://127.0.0.1:7890 all_proxy=socks5://127.0.0.1:7890

# TODO: [2021-06-03] -> 考虑拆分置单独的 `config.py` 文件.
