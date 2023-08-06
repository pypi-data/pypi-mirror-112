# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 10:12:21 2021

@author: Lujx
"""

# pip install requests

import json
import requests


class WxToolsLujx(object):
    def __init__(self, app_id = 'wx0eacccf89fe04cab', app_secret = 'c2d4ea109ed1053594b9939360cc0d36' , open_id = 'o47YY6x7s3tFyvbH0rpq-zAQXbAM',msg='hi,有人闯入你的家!!!!' ):  
        self.app_id = app_id
        self.app_secret = app_secret
        self.open_id = open_id
        self.msg = msg
 

    def sendMsg(self):
        url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={self.app_id}&secret={self.app_secret}'
        resp = requests.get(url).json()
        access_token = resp.get('access_token')
        print(access_token)

        url = f'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={access_token}'

        req_data = {
            "touser":self.open_id,
            "msgtype":"text",
            "text":
            {
                "content":self.msg
                }
            }

        req_str = json.dumps(req_data,ensure_ascii=False)
        req_data = req_str.encode('utf-8')
        requests.post(url,data=req_data)



if __name__ == '__main__':
    s = WxToolsLujx()
    s.sendMsg()


