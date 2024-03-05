"""

深声科技

"""
import hashlib
import math
import random
import time
from rest_framework.views import APIView
from rest_framework.response import Response
import requests

base = "https://api.deepsound.cn"

urls = {
    "test": base + "/v1.0/tts",
    "video": base + "/avatar/v1/2d/video/create",
    "select": base + "/avatar/v1/2d/video/status"
}

'''
生成数字人请求头
'''


def getHeader():
    timer = str(math.floor(time.time()))
    appid = "9C9U0pJl"
    appsecret = "7e7a8f175a1219cdbb1f86666f571353"
    # 创建一个md5 hash对象
    hash_object = hashlib.md5()
    # 更新hash对象
    hash_object.update((appid + timer + appsecret).encode())
    # 获取16进制哈希值并转换为大写
    sign = hash_object.hexdigest().upper()

    header = {"Content-Type": "application/json;charset=utf-8", "X-Deepsound-Sign": "MD5 " + sign,
              "X-Deepsound-Appid": appid, "X-Deepsound-Timestamp": timer}

    return header


class DeepSound(APIView):
    def post(self, request):

        frontend = request.data
        # 使用的数字人模型id
        frontend['model_id'] = '44420'
        # 上传的名称
        frontend['name'] = f'{random.randint(1, 100000)}'

        print('frontend-->', frontend)

        headers = getHeader()

        respone = requests.post(urls.get("video"), json=frontend, headers=headers)

        print("respone--->", respone.json())

        video_id = respone.json()['data']['video_id']

        if respone.status_code == 200:
            return Response("生成中》》》")
        else:
            return Response("生成失败")

    '''
    数字人生成视频查询
    '''

    def get_video(self, video_id):
        frontend = {"video_id": video_id}

        headers = getHeader()

        respone = requests.get(urls.get("select"), params=frontend, headers=headers)

        print("respone--->", respone.json())

        return respone.json()
