from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
# Create your models here.


class UserProfile(AbstractUser):
    """
    用户
    """
    SEX = (
        ("male","男"),
        ("female","女")
    )
    name = models.CharField(max_length=30,null=True,blank=True,verbose_name="姓名")
    birthday = models.DateField(null=True,blank=True,verbose_name="生日")
    gender = models.CharField(choices=SEX,default="male",max_length=15,verbose_name="年龄")
    email = models.EmailField(max_length=50,null=True,blank=True,verbose_name="电子邮箱")
    mobile = models.CharField(max_length=11,verbose_name="手机号")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")


    class Meta:
        verbose_name = "用户信息表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username



class VerifyCode(models.Model):
    """
    用户在注册的时候验证当前用户是否有发送验证码以及验证码的时间问题
    """
    code = models.CharField(max_length=40,verbose_name="验证码")
    mobile = models.CharField(max_length=11,verbose_name="手机号")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")


    class Meta:
        verbose_name = "短信验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
