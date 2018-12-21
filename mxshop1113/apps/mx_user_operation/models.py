from django.db import models
from datetime import datetime

from mx_user.models import UserProfile
from mx_goods.models import Goods
# Create your models here.
class UserAddress(models.Model):
    """
    用户收货地址
    """
    users = models.ForeignKey(UserProfile,verbose_name="用户")
    province = models.CharField(max_length=100,default="",verbose_name="省份")
    city = models.CharField(max_length=100,default="",verbose_name="城市")
    district = models.CharField(max_length=100,default="",verbose_name="区域")
    address = models.CharField(max_length=100,default="",verbose_name="详细地址")
    signer_name = models.CharField(max_length=100,default="",verbose_name="签收人")
    signer_mobile = models.CharField(max_length=100,default="",verbose_name="手机号")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户收货地址"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address

class UserFav(models.Model):
    """
    用户收藏
    """
    users = models.ForeignKey(UserProfile,verbose_name="用户")
    goods = models.ForeignKey(Goods,verbose_name="商品")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")


    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name
        #联合唯一
        unique_together = ("users","goods")

    def __str__(self):
        return self.users.username

class UserLeavingMesage(models.Model):
    """
    用户留言
    """
    MESSAGE_CHOICES = (
        (1, "留言"),
        (2, "投诉"),
        (3, "询问"),
        (4, "售后"),
        (5, "求购")
    )
    users = models.ForeignKey(UserProfile,verbose_name="用户")
    message_type = models.IntegerField(default=1, choices=MESSAGE_CHOICES, verbose_name="留言类型")
    subject = models.CharField(max_length=100,default="",verbose_name="主题")
    message = models.TextField(default="",verbose_name="留言内容")
    file = models.FileField(upload_to='message/images/',verbose_name="上传文件")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户留言"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.users.username

