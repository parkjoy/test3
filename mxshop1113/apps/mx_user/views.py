from django.shortcuts import render

# Create your views here.
from django.contrib.auth.backends import ModelBackend
# from mx_user.models import UserProfile
from django.contrib.auth import get_user_model
from django.db.models import Q
User = get_user_model()
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from mx_user.models import VerifyCode,UserProfile
from mx_user.seriailzers import SendSmsSeriailzer,RegisterSeriailzer,UserDetailSerializer
from utils.yunpian import YunPian
from mxshop1113.settings import API_KEY
from rest_framework import status
from rest_framework.response import Response
from random import choice
from rest_framework_jwt.serializers import jwt_payload_handler,jwt_encode_handler
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import permissions


class CustomBackend(ModelBackend):
   """
   自定义用户验证
   """
   def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

class SendSmsViewset(GenericViewSet,mixins.CreateModelMixin):
    """
    create:创建验证码对象
    """
    #指定序列化器
    serializer_class = SendSmsSeriailzer

    #生成随机验证码4位
    def send_code(self):
        send_str = "0123456789"
        send_rad = []
        #循环4次
        for i in range(4):
            send_rad.append(choice(send_str))

        #列表转成字符串
        return "".join(send_rad)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        #1;发送验证码
        mobile = request.data["mobile"]
        #生成验证码
        code = self.send_code()

        yunpian = YunPian(API_KEY)
        sms_status = yunpian.send_sms(code=code,mobile=mobile)

        #判断 验证码是否发送成功
        if sms_status["code"] != 0:
            #发送失败
            return Response ({
                "msg":sms_status["msg"]
            },status=status.HTTP_400_BAD_REQUEST)
        else:
            #2：将验证码和手机号保存到数据库
            VerifyCode.objects.create(code=code,mobile=mobile)
            return Response({
                "moblie":mobile
            },status=status.HTTP_201_CREATED)
        #3:将结果返回
        #185 114
        #185 220

class UsersViewset(GenericViewSet,mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin):

    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)

    #序列化
    def get_serializer_class(self):
        #注册RegisterSeriailzer
        if self.action == "create":
            return RegisterSeriailzer
        #用户中心
        elif self.action == "retrieve":
            return UserDetailSerializer
        return UserDetailSerializer

    #权限
    def get_permissions(self):
        #注册
        if self.action == "create":
            return []
        #用户中心
        elif self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #user当前注册的用户对象
        user = self.perform_create(serializer)

        #=====写token
        #1:payload = payload(user)
        payload = jwt_payload_handler(user)
        #2：payload--->encode sign加密算法  ---》token
        token = jwt_encode_handler(payload)

        #token赋值
        re_dict = serializer.data
        re_dict["token"] = token
        re_dict["name"] = user.username


        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        #返回的是user对象
        return serializer.save()

    #users/1/  8.9.10  get_object  获取当前登录的用户
    def get_object(self):
        return self.request.user

















