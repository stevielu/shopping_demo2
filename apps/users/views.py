from django.shortcuts import render

# Create your views here.
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status


from rest_framework import permissions
from rest_framework_jwt.serializers import jwt_encode_handler,jwt_payload_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from .serilaizer import UserRegisterSerializer
from .serilaizer import UserDetailsSerializer

User = get_user_model()

class MyLogin(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(mobile=username));
            print(user)
            if user.check_password(password):
                return user
        except Exception as e:
            return None



class UserViewSet(CreateModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,viewsets.GenericViewSet):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailsSerializer
        elif self.action == "create":
            return UserRegisterSerializer

        return UserDetailsSerializer

    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return [permissions.AllowAny]

        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        payload = jwt_payload_handler(user)

        dict = serializer.data
        dict["token"] = jwt_encode_handler(payload)

        headers = self.get_success_headers(serializer.data)
        return Response(dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    def get_object(self):
        return self.request.user