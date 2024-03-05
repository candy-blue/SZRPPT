from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from MainApp.models import Userinfor
from rest_framework.viewsets import GenericViewSet

from MainApp import models

# def Hello(request):
#     users = models.Userinfor.objects.all()
#     lists = users.values()
#     return HttpResponse(lists)
#
#
# def addUser(request):
#     models.Userinfor.objects.create(user_name="陈松韬", user_account='28722', user_pwd='1234')
#     return HttpResponse("创建成功！")


# class UserSerializers(serializers.Serializer):
#     user_name = serializers.CharField(min_length=2, max_length=20)
#     user_account = serializers.CharField(min_length=11, max_length=20)
#     user_pwd = serializers.CharField(min_length=8, max_length=20)
#
#     def create(self, validated_data):
#         new_User = Userinfor.objects.create(**validated_data)
#         return new_User
#
#     def update(self, instance, validated_data):
#         Userinfor.objects.filter(pk=instance.pk).update(**validated_data)
#         new_User = Userinfor.objects.get(pk=instance.pk)
#         return new_User

#
# class UserSerializers(serializers.ModelSerializer):
#     class Mate:
#         model = Userinfor


# class UserView(APIView):
#
#     def get(self, request):
#         user_list = Userinfor.objects.all()
#         serializer = UserSerializers(instance=user_list, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         print(request.data)
#         serializer = UserSerializers(data=request.data)
#
#         if serializer.is_valid():
#
#             serializer.save()
#
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
#         return Response()
#
#     def delete(self, request):
#         return HttpResponse("APIView DELETE...")
#
#     def put(self, request):
#         return Response('')


# class UserView2(APIView):
#
#     def get(self, request, id):
#         user = Userinfor.objects.get(pk=id)
#         serializers = UserSerializers(instance=user, many=False)
#
#         return Response(serializers.data)
#
#     def delete(self, request, id):
#         Userinfor.objects.get(pk=id).delete()
#         return Response()
#
#
#     def put(self, request, id):
#         user = Userinfor.objects.get(pk=id)
#         serializers = UserSerializers(instance=user,data=request.data)
#
#         if serializers.is_valid():
#             serializers.save()
#             return Response(serializers.data)
#         else:
#             return Response(serializers.errors)
#         return Response()


##########################################################################


from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, \
    DestroyModelMixin


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = Userinfor
        fields = '__all__'


class UserView(GenericViewSet, ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin,
               DestroyModelMixin):
    queryset = Userinfor.objects.all()
    serializer_class = UserSerializers


class LoginView(APIView):

    def post(self,request):
        print(request.data)

        account = request.data.get('account')
        pwd = request.data.get('pwd')

        user_object = models.Userinfor.objects.filter(user_account=account,user_pwd=pwd).first()
        if not user_object:
            return Response({"code":1001,'msg':"用户名或密码错误"})

        return Response({"code":1000,'msg':"登陆成功"})

