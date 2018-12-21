# coding=utf-8
from rest_framework import serializers
from mx_user.models import UserProfile,VerifyCode
from mxshop1113.settings import REGEX_MOBILE
import re
from datetime import datetime
from datetime import timedelta
from rest_framework.validators import UniqueValidator

class SendSmsSeriailzer(serializers.Serializer):
    #手机号 required 针对于label都没有输入框    blank针对于表单输入框
    mobile = serializers.CharField(required=True,max_length=11,min_length=11,allow_blank=False,label="手机号",help_text="手机号",error_messages={
        "required":"请输入手机号",
        "max_length":"手机号输入不合法",
        "min_length":"手机号输入不合法",
        "blank":"请输入手机号"
    })

    #验证手机号
    def validate_mobile(self,mobile):
        # 1：验证手机号是否注册过
        if UserProfile.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已存在")
        # 2：验证手机号是否合法 m 从头 None  s 全局 if not None:
        if not re.match(REGEX_MOBILE,mobile):
            raise serializers.ValidationError("手机号不合法")
        # 3：当前这个手机号的验证码距离上一次发送的时间？？？60s
        #11:44:30  11:43:30  11:43:20可以发送  11:43:50还没有到60s
        one_min_ago = datetime.now()-timedelta(hours=0,minutes=1,seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_min_ago,mobile=mobile).count():
            raise serializers.ValidationError("距离上一次发送还未到60s")

class RegisterSeriailzer(serializers.ModelSerializer):
    code = serializers.CharField(min_length=4,max_length=4,label="验证码",help_text="验证码",write_only=True,required=True,allow_blank=False,error_messages={
        "required":"请输入验证码",
        "max_length":"验证码输入不合法",
        "min_length":"验证码输入不合法",
        "blank":"请输入验证码"
    })
    username = serializers.CharField(max_length=11,min_length=11,required=True,allow_blank=True,label="用户名",help_text="用户名",validators=[UniqueValidator(queryset=UserProfile.objects.all(),message="用户已存在")])

    password = serializers.CharField(max_length=20,label="密码",write_only=True,style={'input_type': 'password'},help_text="密码")

    mobile = serializers.CharField(allow_blank=True,write_only=True,allow_null=True,help_text="手机号")


    # def create(self, validated_data):
    #     #重写create方法
    #     user = super(RegisterSeriailzer, self).create(validated_data=validated_data)
    #     #密码加密
    #     user.set_password(validated_data["password"])
    #     user.save()
    #     return user



    def validate_code(self,code):
        #1：是否存在
        verify_code = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")
        if verify_code:
            last_code = verify_code[0]
            # 2: 验证码是错误
            if last_code.code != code:
                raise serializers.ValidationError("验证码是错误")
            # 3：过期时间  #14:56:30  14:51:30 14:51:25 过期   14:51:35
            five_min_ago = datetime.now() - timedelta(hours=0,minutes=5,seconds=0)
            if five_min_ago > last_code.add_time:
                raise serializers.ValidationError("验证码已经过期")
        else:
            raise serializers.ValidationError("手机号未发送过验证码")

    def validate(self, attrs):
        #将username的值赋值给手机号
        attrs["mobile"]= attrs["username"]
        #删除code
        del attrs["code"]
        return attrs


    class Meta:
        model = UserProfile
        fields = ("username","code","password","mobile")

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("name","birthday","gender","email","mobile")


