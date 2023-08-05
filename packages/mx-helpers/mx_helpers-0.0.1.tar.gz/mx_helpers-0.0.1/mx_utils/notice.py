# -*- coding: utf-8 -*-
# @Time    : 2021/6/24 9:50 上午
# @Author  : X.Lin
# @Email   : ****
# @File    : notice.py
# @Software: PyCharm
# @Desc    : 通知模块
import json
import time
import base64, hashlib, hmac, urllib.parse
import requests

class DDing:
    """
    机器人创建/使用说明:

    创建/添加群聊机器人: 群聊 -> 更多 -> 群助手 -> 添加群聊机器人 -> 自定义[通过Webhook接入]
    群聊机器人配置: 安装设置 -> √ 加签
    webhook: 机器人设置页面 -> webhook
    secret: 机器人设置页面 -> 勾选"加签" -> 底下的字符串
    """

    def __init__(self, webhook: str, secret: str, isAtAll: bool = True):
        """

        :param webhook:
        :param secret:
        :param isAtAll:  是否@所有人。
        """
        self._mSecret = secret
        self._mWebhook = webhook
        self._mIsAtAll = isAtAll

    def getSign(self):
        timestamp = str(round(time.time() * 1000))
        secret = self._mSecret
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return timestamp, sign

    def sendMessage(self, data) -> bool:
        """
        发送Text文本消息
        :param data: 发送的文本消息.
        :return: 是否发送成功
        """
        timestamp, sign = self.getSign()
        headers={'Content-Type': 'application/json'}
        webhook = self._mWebhook + '&timestamp=' + timestamp + "&sign=" + sign
        data = {"msgtype": "text", "text": {"content": data}, "isAtAll": self._mIsAtAll}    # 是否@所有人。
        res = requests.post(webhook, data=json.dumps(data), headers=headers)
        return res.json()['errcode'] == 0