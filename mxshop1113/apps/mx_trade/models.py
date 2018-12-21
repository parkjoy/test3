from django.db import models

from datetime import datetime
from mx_user.models import UserProfile
from mx_goods.models import Goods
# Create your models here.
class ShoppingCart(models.Model):
    """
    购物车
    """
    user = models.ForeignKey(UserProfile,verbose_name="用户")
    goods = models.ForeignKey(Goods,verbose_name="商品")
    goods_num = models.IntegerField(default=0,verbose_name="商品个数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "购物车"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username


class OrderInfo(models.Model):
    """
    订单
    """
    order_status = (
        ("TRADE_SUCCESS", "成功"),
        ("TRADE_CLOSED", "超时关闭"),
        ("WAIT_BUYER_PAY", "交易创建"),
        ("TRADE_FINISHED", "交易结束"),
        ("paying", "待支付"),
    )
    user = models.ForeignKey(UserProfile, verbose_name="用户")
    order_sn = models.CharField(null=True,blank=True,max_length=200,verbose_name="订单号")
    trade_no = models.CharField(max_length=200,null=True,blank=True,verbose_name="支付宝交易号")
    pay_status = models.CharField(max_length=100,choices=order_status,default="paying",verbose_name="支付状态")
    post_script = models.CharField(max_length=200,verbose_name="订单留言",default="")
    order_mount = models.FloatField(verbose_name="订单总金额",default=0.0)
    pay_time = models.DateTimeField(null=True,blank=True,verbose_name="支付时间")

    #用户信息
    address = models.CharField(max_length=100,default="",verbose_name="收货地址")
    signer_name = models.CharField(max_length=20,default="",verbose_name="收货人姓名")
    singer_moblie = models.CharField(max_length=11,verbose_name="手机号",default="")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "订单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username


class OrderGoods(models.Model):
    """
    订单详情
    """
    order = models.ForeignKey(OrderInfo,verbose_name="订单信息",related_name="order_goods")
    goods = models.ForeignKey(Goods,verbose_name="商品")
    goods_num = models.IntegerField(default=0,verbose_name="商品数量")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "订单详情"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order.order_sn
