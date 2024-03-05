from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, \
    DestroyModelMixin
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from MainApp.models import Userinfor, UserProject
from rest_framework.viewsets import GenericViewSet

from MainApp import models


class ProjectSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProject
        fields = '__all__'


class ProjectView(GenericViewSet, ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin,
                  DestroyModelMixin):
    queryset = UserProject.objects.all()
    serializer_class = ProjectSerializers


class Ppt_Upload(APIView):
    def post(self, request):
        user_id = request.data["user_id"]
        project_name = request.data["project_name"]

        project = models.UserProject.objects.create(user_id=user_id, project_name=project_name)

        print(project)

        return Response("陈松韬")
