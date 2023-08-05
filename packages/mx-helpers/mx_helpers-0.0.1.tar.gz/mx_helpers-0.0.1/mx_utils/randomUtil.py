# -*- coding: utf-8 -*-
# @Time    : 2021/6/4 10:32 上午
# @Author  : X.Lin
# @Email   : ****
# @File    : randomUtil.py
# @Software: PyCharm
# @Desc    : 生成`随机`数据工具类.
import string
import random
_DIGITS_LIST = string.digits


def genRandomNumber(count: int = 4) -> int:
    """
    生成随机数字.
    :param count: 数字个数. 默认: 4
    :return:
    """
    rets = [random.choice(_DIGITS_LIST) for i in range(count)]
    return int(''.join(rets))