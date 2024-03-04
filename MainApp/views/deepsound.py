"""

深声科技

"""
import hashlib
import math
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
        headers = getHeader()

        respone = requests.post(urls.get("video"), json=frontend, headers=headers)

        print("respone--->", respone.json())

        if respone.status_code == 200:
            return Response(respone.json())
        else:
            return Response(respone.json())

    def get(self, request):
        frontend = { "video_id":request.GET.get('video_id')}

        headers = getHeader()

        respone = requests.get(urls.get("select"), params=frontend, headers=headers)

        print("respone--->", respone.json())

        if respone.status_code == 200:
            return Response(respone.json())
        else:
            return Response(respone.json())
