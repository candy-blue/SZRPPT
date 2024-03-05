import mimetypes
import shutil
import office
import pofile
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import os

from MainApp.models import UserProject
from MainApp.views import Qiniu

# ppt存放文件夹
ppt_dir = r'D:\pythonProject save\SZRPPT\static\ppt'
# 图片存放文件夹
jpg_dir = r'D:\pythonProject save\SZRPPT\static\jpg'

'''
ppt转图片:
用户在前端选择创建项目后选择ppt文件和项目名称
后选择发送到后端
后端接收请求并验证无误后
先在数据库创建新的项目数据,然后将项目id返回
同时将ppt转图片后的图片文件通过Qiniu.upload上传到云端,并将图片的url保存为列表
图片全部上传后,更新用户项目表的image_list
'''
class PPTtoImages(APIView):
    def post(self, request):

        print("request.data--->", request.data)
        print("request.FILES--->", request.FILES.get("ppt"))

        ppt = request.FILES.get("ppt")

        # 检查是否接收到了文件
        ppt_pd(ppt)

        user_id = int(request.data['user_id'])
        project_name = request.data['project_name']

        # 检查项目名称是否已存在
        if UserProject.objects.filter(user_id=user_id, project_name=project_name).exists():
            return Response({'error': '该项目名称已存在'}, status=status.HTTP_400_BAD_REQUEST)

        project = UserProject.objects.create(user_id=user_id, project_name=project_name)

        pptx_file = request.FILES.get("ppt")
        project_id = project.project_id

        # 保存接收的ppt文件到本地
        PptSave(pptx_file)
        # 进行ppt转图片并返回图片列表
        image_list = PpttoImage()

        urls = []

        for i, path in enumerate(image_list):
            ret = Qiniu.upload(i, path, user_id=user_id, project_id=project_id, type="image")
            url = "http://s8xw6kecm.hn-bkt.clouddn.com/" + ret['key']
            urls.append(url)

        delete_files(jpg_dir)
        delete_files(ppt_dir)

        project.image_list = f'{urls}'
        project.save()

        return Response({'message': '上传成功', "image": f'{urls}'}, status=status.HTTP_200_OK)

    def get(self, request):
        user_id = request.data["user_id"]
        project_id = request.data["project_id"]
        type = "image"
        urls = Qiniu.download_folder(user_id, project_id, type)
        return Response({"urls": urls})


'''判断是否发送文件过来以及是否为ppt文件'''
def ppt_pd(ppt):
    if not ppt:
        return Response({'error': '没有文件!'}, status=status.HTTP_400_BAD_REQUEST)

    mime_type = mimetypes.guess_type(ppt.name)[0]

    # 检查MIME类型是否为PPT文件
    if not mime_type or mime_type not in ['application/vnd.ms-powerpoint',
                                          'application/vnd.openxmlformats-officedocument.presentationml.presentation']:
        return Response({'error': '文件不是有效的PPT文件!'}, status=status.HTTP_400_BAD_REQUEST)


'''PPT转图片'''
def PpttoImage():
    if not os.path.exists(jpg_dir):
        os.makedirs(jpg_dir)

    office.ppt.ppt2img(input_path=f'D:\\pythonProject save\\SZRPPT\\static\\ppt',
                       output_path=f'D:\\pythonProject save\\SZRPPT\\static\\jpg',
                       merge=False)

    images = pofile.get_files(path=f'D:\\pythonProject save\\SZRPPT\\static\\jpg', suffix='JPG')

    return images


'''接收ppt并保存到本地'''
def PptSave(pptx_file):
    if not os.path.exists(ppt_dir):
        os.makedirs(ppt_dir)

    file_path = os.path.join(ppt_dir, pptx_file.name)

    with open(file_path, 'wb') as f:
        for ppt in pptx_file.chunks():
            f.write(ppt)

    print("ppt接收成功")


'''删除目录中的所有文件'''
def delete_files(folder_path):
    # 检查文件夹是否存在
    if os.path.exists(folder_path):
        # 如果文件夹存在，则删除它及其内容
        shutil.rmtree(folder_path)
        print("内容已删除。")
