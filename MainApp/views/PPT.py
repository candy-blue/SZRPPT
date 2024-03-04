import shutil
import office
import pofile
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import os
from MainApp.views import Qiniu

# ppt存放文件夹
ppt_dir = r'D:\pythonProject save\SZRPPT\static\ppt'
# 图片存放文件夹
jpg_dir = r'D:\pythonProject save\SZRPPT\static\jpg'


class PPTtoImages(APIView):
    def post(self, request):

        # 检查是否接收到了文件
        if 'ppt' not in request.FILES:
            return Response({'error': '没有ppt文件'}, status=status.HTTP_400_BAD_REQUEST)

        pptx_file = request.FILES['ppt']
        user_id = request.data['user_id']
        project_id = request.data['project_id']

        print(request.data)

        # 保存接收的ppt文件到本地
        self.PptSave(pptx_file)
        # 进行ppt转图片并返回图片列表
        image_list = self.PpttoImage()

        urls = []

        for i, path in enumerate(image_list):
            ret = Qiniu.upload(i, path, user_id=user_id, project_id=project_id, type="image")
            url = "http://s8xw6kecm.hn-bkt.clouddn.com/" + ret['key']
            urls.append(url)

        self.delete_files(jpg_dir)
        self.delete_files(ppt_dir)
        return Response({'message': '上传成功', "image": f'{urls}'}, status=status.HTTP_200_OK)

    def get(self, request):
        user_id = request.data["user_id"]
        project_id = request.data["project_id"]
        type = "image"
        urls = Qiniu.download_folder(user_id, project_id, type)
        return Response({"urls": urls})

    # PPT转图片
    def PpttoImage(self):
        if not os.path.exists(jpg_dir):
            os.makedirs(jpg_dir)

        office.ppt.ppt2img(input_path=f'D:\\pythonProject save\\SZRPPT\\static\\ppt',
                           output_path=f'D:\\pythonProject save\\SZRPPT\\static\\jpg',
                           merge=False)

        images = pofile.get_files(path=f'D:\\pythonProject save\\SZRPPT\\static\\jpg', suffix='JPG')

        return images

    # 接收ppt并保存
    def PptSave(self, pptx_file):

        if not os.path.exists(ppt_dir):
            os.makedirs(ppt_dir)

        file_path = os.path.join(ppt_dir, pptx_file.name)

        with open(file_path, 'wb') as f:
            for ppt in pptx_file.chunks():
                f.write(ppt)

        print("ppt接收成功")

    # 删除目录中的所有文件
    def delete_files(self, folder_path):
        # 检查文件夹是否存在
        if os.path.exists(folder_path):
            # 如果文件夹存在，则删除它及其内容
            shutil.rmtree(folder_path)
            print("内容已删除。")
