from django.db import models


# Create your models here.


class Userinfor(models.Model):
    user_id = models.AutoField(primary_key=True, verbose_name="用户id")
    user_name = models.CharField(verbose_name="用户名", max_length=20)
    user_account = models.CharField(verbose_name="用户账号", max_length=20)
    user_pwd = models.CharField(verbose_name="用户密码", max_length=20)


# 用户项目模型
class UserProject(models.Model):
    project_id = models.AutoField(primary_key=True, verbose_name="项目id")
    project_name = models.CharField(verbose_name="项目名称",max_length=255)
    user_id = models.IntegerField(verbose_name="用户id")
    image_list = models.TextField(verbose_name="图片列表",null=True)


# 项目信息模型
# class ProjectInfo(models.Model):
