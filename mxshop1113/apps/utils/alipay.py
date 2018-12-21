# -*- coding: utf-8 -*-

# pip install pycryptodome

from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64encode, b64decode
from urllib.parse import quote_plus
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen
from base64 import decodebytes, encodebytes

import json


class AliPay(object):
    """
    支付宝支付接口
    """
    def __init__(self, appid, app_notify_url, app_private_key_path,
                 alipay_public_key_path, return_url, debug=False):
        self.appid = appid
        self.app_notify_url = app_notify_url
        self.app_private_key_path = app_private_key_path
        self.app_private_key = None
        self.return_url = return_url

        #读出txt中的商户私钥，使用RSA进行加密
        with open(self.app_private_key_path) as fp:
            self.app_private_key = RSA.importKey(fp.read())

        #读出txt中的支付宝公钥，使用RSA进行加密
        self.alipay_public_key_path = alipay_public_key_path
        with open(self.alipay_public_key_path) as fp:
            self.alipay_public_key = RSA.import_key(fp.read())


        #沙箱环境
        if debug is True:
            self.__gateway = "https://openapi.alipaydev.com/gateway.do"
        # 正式环境
        else:
            self.__gateway = "https://openapi.alipay.com/gateway.do"


    #接收业务参数
    def direct_pay(self, subject, out_trade_no, total_amount, return_url=None, **kwargs):
        biz_content = {
            #主题
            "subject": subject,
            #订单号
            "out_trade_no": out_trade_no,
            #总价
            "total_amount": total_amount,
            "product_code": "FAST_INSTANT_TRADE_PAY",
            # "qr_pay_mode":4
        }
        #添加额外参数 不是必填项
        biz_content.update(kwargs)

        #填写公共参数
        data = self.build_body("alipay.trade.page.pay", biz_content, self.return_url)
        #请求签名
        return self.sign_data(data)


    #公共参数
    def build_body(self, method, biz_content, return_url=None):
        data = {
            "app_id": self.appid,
            "method": method,
            "charset": "utf-8",
            "sign_type": "RSA2",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": "1.0",
            "biz_content": biz_content
        }


        if return_url is not None:
            data["notify_url"] = self.app_notify_url
            data["return_url"] = self.return_url

        return data


    #请求签名1
    def sign_data(self, data):
        data.pop("sign", None)
        # 排序后的字符串
        unsigned_items = self.ordered_data(data)
        #将排序后的参数与其对应值，组合成“参数=参数值”的格式，并且把这些参数用&字符连接起来
        unsigned_string = "&".join("{0}={1}".format(k, v) for k, v in unsigned_items)
        #使用各自语言对应的SHA256WithRSA(对应sign_type为RSA2)或SHA1WithRSA(对应sign_type为RSA)签名函数利用商户私钥对待签名字符串进行签名，并进行Base64编码。
        sign = self.sign(unsigned_string.encode("utf-8"))

        ordered_items = self.ordered_data(data)
        quoted_string = "&".join("{0}={1}".format(k, quote_plus(v)) for k, v in ordered_items)

        # 获得最终的订单信息字符串
        signed_string = quoted_string + "&sign=" + quote_plus(sign)
        return signed_string

    #排序
    def ordered_data(self, data):
        complex_keys = []
        for key, value in data.items():
            if isinstance(value, dict):
                complex_keys.append(key)

        # 将字典类型的数据dump出来
        for key in complex_keys:
            data[key] = json.dumps(data[key], separators=(',', ':'))

        return sorted([(k, v) for k, v in data.items()])

    #签名
    def sign(self, unsigned_string):
        # 开始计算签名
        key = self.app_private_key
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(SHA256.new(unsigned_string))
        # base64 编码，转换为unicode表示并移除回车
        sign = encodebytes(signature).decode("utf8").replace("\n", "")
        return sign

    def _verify(self, raw_content, signature):
        # 开始计算签名
        key = self.alipay_public_key
        signer = PKCS1_v1_5.new(key)
        digest = SHA256.new()
        digest.update(raw_content.encode("utf8"))
        if signer.verify(digest, decodebytes(signature.encode("utf8"))):
            return True
        return False

    def verify(self, data, signature):
        if "sign_type" in data:
            sign_type = data.pop("sign_type")
        # 排序后的字符串
        unsigned_items = self.ordered_data(data)
        message = "&".join(u"{}={}".format(k, v) for k, v in unsigned_items)
        return self._verify(message, signature)


if __name__ == "__main__":
    return_url = "http://127.0.0.1:8000/alipay/return/?charset=utf-8&out_trade_no=20181218113440173&method=alipay.trade.page.pay.return&total_amount=15.00&sign=m1Qov9J98tXEzWlWd16eMtyjx0mfw0b3F1cHUGDlKeNZg7TYwPUbvFYHWJL494W8iL3ANoTuxcM0MR13iH6asdBxbgBCScYh2%2BKxfiM%2FBomW8yRf2WT0cbVSdFYsvWgQgSnar%2BhGO8hMlhE7pk0RxK0DLpW1Iz2zLVceX4Iivv3o44x5JvRDH00WZr8gSeV4nWSQ0RvbIDAli1yg1jOwJXUfFiYt28pMmrK6NfIa2LDYmetoMPl2gKQ8qz4BEWn7wpmOjpkTCRWObvoU%2Brr4Fe%2FN2Eglj%2F%2B4jmMJUBdHn6WfvtZjHVNmvhNYP%2BsWBxx%2FDCM%2B3CKuQoTM7PzwDSQe1g%3D%3D&trade_no=2018121822001447510500644575&auth_app_id=2016092400582020&version=1.0&app_id=2016092400582020&sign_type=RSA2&seller_id=2088102176992883&timestamp=2018-12-18+11%3A35%3A59"
    alipay = AliPay(
        #支付宝的appid
        appid="2016091700530650",
        #暂时
        app_notify_url="http://127.0.0.1:8000/alipay/return/",
        #商户的私钥
        app_private_key_path="../mx_trade/keys/private_2048.txt",
        #支付宝的公钥
        alipay_public_key_path="../mx_trade/keys/alipay_key_2048.txt",  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        #环境
        debug=True,  # 默认False,
        #暂时
        return_url="http://127.0.0.1:8000/alipay/return/"
    )

    o = urlparse(return_url)
    query = parse_qs(o.query)
    processed_query = {}
    ali_sign = query.pop("sign")[0]
    for key, value in query.items():
        processed_query[key] = value[0]
    print (alipay.verify(processed_query, ali_sign))

    # url = alipay.direct_pay(
    #     #订单标题
    #     subject="测试订单",
    #     #商户订单号
    #     out_trade_no="201702021882",
    #     #订单总金额
    #     total_amount=0.01
    # )
    #
    # #url 生成支付宝订单二维码的url
    # re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
    # print(re_url)