import requests

class YunPian(object):
    def __init__(self,api_key):
        #发送接口的url
        self.send_url = "https://sms.yunpian.com/v2/sms/single_send.json"
        #api_key 必填
        self.apikey = api_key

    def send_sms(self,code,mobile):
        #post参数
        parms = {
            "apikey":self.apikey,
            "mobile":mobile,
            "text":"【小镇生活】小镇生活，您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code)
        }
        #发送post请求
        response = requests.post(self.send_url,data=parms)
        import json  #<response 200>
        re_dict = json.loads(response.text)
        return re_dict


if __name__ == '__main__':
    yunpian = YunPian("d47387abfe0eca2c0ac56591a5ae59e9")
    yunpian.send_sms("2018","18514050680")


