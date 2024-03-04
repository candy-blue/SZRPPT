import os
import subprocess
import cv2
import numpy as np
import urllib.request
import ffmpeg

"""
删除文件函数

在执行函数后删除生成的素材文件


"""


def remove_file():
    if os.path.exists(output_video_path):
        os.remove(output_video_path)


# 输出文件路径
output_video_path = r'D:\pythonProject save\SZRPPT\static\output\testvideo.mp4'
# 视频列表文件路径
text_file = r'D:\pythonProject save\SZRPPT\static\output\list.txt'
# 最终合成的视频路径
output_file = r'D:\pythonProject save\SZRPPT\static\output\max_video.mp4'
"""

多个视频合成

"""


def videos_hc(videos):
    with open(text_file, 'w') as file_list:
        for video in videos:
            file_list.write(f'file \'{video}\'\n')

    ffmpeg_cmd = ['ffmpeg', '-f', 'concat','-i', text_file, '-c', 'copy', output_file]

    # 调用ffmpeg命令
    subprocess.run(ffmpeg_cmd, check=True)

    # 删除临时文件
    # os.remove(text_file)

    print("视频合成完成")

"""
获取视频高度

image_path:输入图片链接
"""


def get_height(image_url):
    # 从 URL 中读取图像数据
    resp = urllib.request.urlopen(image_url)
    image_data = resp.read()

    # 将图像数据解码为 OpenCV 图像格式
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)

    # 获取图像高度
    height = img.shape[0]

    return height


"""
图片视频合成


image:图片链接

output_video_path:数字人绿幕视频路径
image_path:背景图片路径
"""


def video_with_image(input_video_path, image_path):
    image_height = get_height(image_path)

    # FFmpeg命令：将透明视频叠加在静态图像上
    ffmpeg_command = [
        'ffmpeg', '-loop', '1',
        '-i', image_path,
        '-i', input_video_path,
        '-filter_complex',
        f'[1:v]chromakey=color=#58da94:similarity=0.1,format=rgba,scale=-1:{image_height}[bg];'
        f'[0:v][bg]overlay=W-w:H-h[outv]',
        '-map', '[outv]',
        '-map', '1:a?',  # 保留原视频的音频流
        '-c:v', 'libx264', '-preset', 'ultrafast',
        '-c:a', 'copy',  # 复制原视频的音频编码，而不是重新编码
        '-shortest',
        output_video_path
    ]

    # 执行FFmpeg命令
    subprocess.run(ffmpeg_command)

    print("视频生成完成!")


def main_video(v1, image):
    remove_file()
    video_with_image(v1, image)


# main_video("http://s9m40p7q7.hn-bkt.clouddn.com/video.mp4",
#            "http://s9m40p7q7.hn-bkt.clouddn.com/wallhaven-jxqd2m.jpg")


# 视频文件列表
video_files = ['http://s9m40p7q7.hn-bkt.clouddn.com/1.mp4', 'http://s9m40p7q7.hn-bkt.clouddn.com/2.mp4']


videos_hc(video_files)
