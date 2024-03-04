import os
import win32com.client
from PIL.Image import Image


def ppt2png(ppt_path):
    """
    ppt 转 png 方法
    :param ppt_path: ppt 文件的绝对路径
    :param long_sign: 是否需要转为生成长图的标识
    :return:
    """
    if os.path.exists(ppt_path):
        # 图片输出路径
        output_path = f'D:\\pythonProject save\\SZRPPT\\static\\ppt-png'

        ppt_app = win32com.client.Dispatch('PowerPoint.Application')
        ppt = ppt_app.Presentations.Open(ppt_path)  # 打开 ppt
        ppt.SaveAs(output_path, 17)  # 17数字是转为 ppt 转为图片
        ppt_app.Quit()  # 关闭资源，退出

    else:
        raise Exception('请检查文件是否存在！\n')


ppt2png('D:\\pythonProject save\\SZRPPT\\static\\123.pptx')