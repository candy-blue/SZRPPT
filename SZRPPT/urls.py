"""
URL configuration for SZRPPT project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from MainApp.views import views, PPT, Qiniu, deepsound

from rest_framework import routers

router = routers.DefaultRouter()
router.register("main/user", views.UserView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.LoginView.as_view()),
    # ppt上传路由
    path('main/ppt', PPT.PPTtoImages.as_view()),
    # 数字人视频路由
    path('main/deepsound', deepsound.DeepSound.as_view()),
    # 文件上传路由
    path('main/upload', Qiniu.upload)


    # path('main/user/', views.UserView.as_view({
    #     "get": "list",
    #     "post": "create"
    # })),
    # re_path('main/user/(?P<pk>\d+)', views.UserView.as_view({
    #     "get": "retrieve",
    #     "delete": "destroy",
    #     "put": "update"
    # }))
]

urlpatterns += router.urls
