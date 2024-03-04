import shutil
import office
import pofile
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import os
from MainApp.views import Qiniu

# ppt存放文件夹
ppt_dir = './static/ppt'
png_dir = './static/ppt-png'
if not os.path.exists(ppt_dir):
    os.makedirs(ppt_dir)


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
        imagelist = self.PpttoImage()


        # self.delete_files(ppt_dir)

        for i, path in enumerate(imagelist):
            Qiniu.upload(i, path, user_id=user_id, project_id=project_id,type="image")

        self.delete_all_contents(png_dir)
        return Response({'message': '图片文件上传成功'}, status=status.HTTP_200_OK)

    def get(self, request):
        user_id = request.data["user_id"]
        project_id = request.data["project_id"]
        type = "image"
        urls = Qiniu.download_folder(user_id, project_id,type)
        return Response({"urls":urls})

    # PPT转图片
    def PpttoImage(self):
        office.ppt.ppt2img(input_path=f'D:\\pythonProject save\\SZRPPT\\static\\ppt',
                           output_path=f'D:\\pythonProject save\\SZRPPT\\static\\ppt-png',
                           merge=False)

        images = pofile.get_files(path=f'D:\\pythonProject save\\SZRPPT\\static\\ppt-png', suffix='JPG')

        return images

    # 接收ppt并保存
    def PptSave(self, pptx_file):

        file_path = os.path.join(ppt_dir, pptx_file.name)

        with open(file_path, 'wb') as f:
            for ppt in pptx_file.chunks():
                f.write(ppt)

        print("ppt接收成功")

    # 删除目录中的所有文件
    def delete_files(self, directory_path):
        # 列出目录中的所有文件
        files = os.listdir(directory_path)
        # 逐个删除文件
        for file_name in files:
            file_path = os.path.join(directory_path, file_name)
            os.remove(file_path)

    # 删除目录中的所有文件,包括文件夹
    def delete_all_contents(self, directory_path):
        # 递归删除目录及其内容
        shutil.rmtree(directory_path)
