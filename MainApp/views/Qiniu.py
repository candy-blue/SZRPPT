"""
七牛云文件存储
"""
import base64
import hashlib
import hmac

from qiniu import Auth, put_file, etag, BucketManager
import qiniu.config

access_key = 'jWlRY2CYSlqb5mnGGXh32i3Rn-UC9nMrkO75Bj3r'
secret_key = 'zdw_190L_xmrKU5kXlSTJup2epeImVdNi6_7b0DT'

# 构建鉴权对象
q = Auth(access_key, secret_key)
# 要上传的空间
bucket_name = 'test-upload15'

'''
七牛云文件上传

file_name:上传的文件名
localfile:
user_id:上传文件的用户id
project_id:上传文件的用户项目id
type:上传的文件类型用于分类 image,audio,video
'''


def upload(file_name, localfile, user_id, project_id, type):
    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    key = f"{user_id}/{project_id}/{type}/{file_name}"

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)

    # 上传文件到七牛云
    ret, info = put_file(token, key, localfile, version='v2')

    # 打印上传结果信息
    # print('info-->',info)
    # print('ret-->', ret)

    # 检查上传是否成功
    if info.status_code == 200:
        print("File uploaded successfully!")
    else:
        print("Failed to upload file:", info.text)

    # 返回上传结果
    return ret


def download_folder(user_id, project_id, type):
    q = Auth(access_key, secret_key)

    # 初始化 BucketManager
    bucket_manager = BucketManager(q)

    # 设置文件夹的前缀，例如 'folder_name/'
    folder_prefix = f'{user_id}/{project_id}/{type}'

    # 分页获取文件夹中的文件列表
    marker = None
    limit = 1000  # 每次获取的最大文件数量，根据实际需求调整
    file_urls = []

    ret, a, b = bucket_manager.list(bucket=bucket_name, prefix=folder_prefix, marker=marker, limit=limit)
    # 获取到的文件列表
    for file_info in ret['items']:
        key = file_info['key']
        # 构建图片的完整 URL
        url = f"http://s8xw6kecm.hn-bkt.clouddn.com/{key}"

        # h = hmac.new(secret_key.encode('utf-8'), url.encode('utf-8'), hashlib.sha1)
        # # 计算签名
        # Sign = h.digest()
        # # 对签名进行URL安全的Base64编码
        # EncodedSign = base64.urlsafe_b64encode(Sign).decode('utf-8').rstrip('=')
        # token2 = f'{access_key}:{EncodedSign}'
        # RealDownloadUrl = f"{url}&token={token2}"

        file_urls.append(url)

    print(file_urls)
    return file_urls
