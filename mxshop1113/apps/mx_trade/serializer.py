# coding=utf-8
from rest_framework import serializers

from mx_goods.models import Goods
from mx_goods.serializers import GoodsListSerializer
from mx_trade.models import ShoppingCart,OrderInfo,OrderGoods




from random import Random
import time
from utils.alipay import AliPay
from datetime import datetime
from mxshop1113.settings import private_key_path,ali_pub_key_path

#购物车详情
class ShoppingCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsListSerializer()
    class Meta:
        model = ShoppingCart
        fields = ("goods","goods_num","id")

#购物车表  post 表单
class ShoppingCartSerializer(serializers.Serializer):
    #用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    #时间
    add_time = serializers.DateTimeField(read_only=True,format="%Y-%m-%d %H:%M")
    #购买的商品个数
    goods_num = serializers.IntegerField(required=True,min_value=1,label="商品个数",error_messages={
        "required":"请至少输入一个商品",
        "min_value":"请至少输入一个商品",
    })
    #商品  外键  id 是否存在商品表
    goods = serializers.PrimaryKeyRelatedField(required=True,queryset=Goods.objects.all(),label="商品")


    #创建购物车商品数据
    def create(self, validated_data):
        #request 上下文中
        user = self.context["request"].user

        #商品个数
        goods_num = validated_data["goods_num"]

        #商品对象
        goods = validated_data["goods"]

        #当前购买的商品是否存在于数据库中
        shop_cart = ShoppingCart.objects.filter(goods=goods,user=user)
        #shop_cart  []  [object]
        if shop_cart:
            #用户购买过此商品
            shop_cart1 = shop_cart[0]
            #添加数量
            shop_cart1.goods_num +=goods_num
            shop_cart1.save()
        else:
            #创建记录
            shop_cart1 = ShoppingCart.objects.create(**validated_data)
        return shop_cart1

    #修改商品数量
    def update(self, instance, validated_data):
        instance.goods_num = validated_data["goods_num"]
        instance.save()
        return instance

#添加订单
class OrderInfoSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # 时间
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M")
    order_sn = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    pay_status = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M")
    #read_only 反序列化
    alipay_url = serializers.SerializerMethodField(read_only=True)

    #生成订单支付二维码url
    def get_alipay_url(self, obj):
        #实例化
        alipay = AliPay(
            # 支付宝的appid
            appid="2016091700530650",
            # 暂时
            app_notify_url="http://127.0.0.1:8000/alipay/return/",
            # 商户的私钥
            app_private_key_path=private_key_path,
            # 支付宝的公钥
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            # 环境
            debug=True,  # 默认False,
            # 暂时
            return_url="http://127.0.0.1:8000/alipay/return/"
        )
        #post 请求参数
        url = alipay.direct_pay(
            # 订单标题
            subject=obj.order_sn,
            # 商户订单号
            out_trade_no=obj.order_sn,
            # 订单总金额
            total_amount=obj.order_mount
        )

        # url 生成支付宝订单二维码的url
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        return re_url


    #生成订单号
    def get_order_code(self):
        random_ins = Random()

        #时间+用户id+两位随机的数字
        order_code = "{time_str}{user_id}{random_str}".format(
            time_str = time.strftime("%Y%m%d%H%M%S"),
            user_id = self.context["request"].user.id,
            random_str = random_ins.randint(10,99)
        )
        return order_code

    #自定义逻辑验证
    def validate(self, attrs):
        attrs["order_sn"] = self.get_order_code()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"

    # 订单详情

#订单商品
class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsListSerializer(many=False)
    class Meta:
        model = OrderGoods
        fields = "__all__"


#订单列表展示
class OrderInfoDetailSerializer(serializers.ModelSerializer):
    order_goods = OrderGoodsSerializer(many=True)
    class Meta:
        model = OrderInfo
        fields = "__all__"








