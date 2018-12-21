from django.shortcuts import render,redirect

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated

from mx_trade.models import ShoppingCart,OrderInfo,OrderGoods
from mx_trade.serializer import ShoppingCartSerializer,ShoppingCartDetailSerializer,OrderInfoSerializer,OrderInfoDetailSerializer

#购物车
class ShoppingCartViewset(viewsets.ModelViewSet):
    """
    list:
        购物车列表
    create:
        添加购物车商品
    delete:
        删除购物车商品
    update:
        修改购物车商品
    """
    authentication_classes = (SessionAuthentication,JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated,)


    lookup_field = "goods_id"


    #添加商品-库存
    def perform_create(self, serializer):
        ins = serializer.save()
        ins.goods.goods_num -=ins.goods_num
        ins.goods.save()

    #删除商品 +1库存
    def perform_destroy(self, instance):
        instance.goods.goods_num += instance.goods_num
        instance.goods.save()
        instance.delete()

    #修改商品数量
    def perform_update(self, serializer):
        # 获取修改之前的商品数量
        shop_cart = ShoppingCart.objects.get(id = serializer.instance.id)
        nums = shop_cart.goods
        # 获取修改之后的商品的个数
        ins = serializer.save()

        # 用修改后的商品个数 减去修改前的个数
        shop_cart_nums = ins.goods_num - nums
        ins.goods.goods_num -= shop_cart_nums
        ins.goods.save()


    def get_serializer_class(self):
        if self.action == "list":
            return ShoppingCartDetailSerializer
        else:
            return ShoppingCartSerializer


    #获取当前登录用户购物车表
    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)


#订单
class OrderInfoViewset(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
    """
    list:
       订单列表
    create:
        添加订单
    delete:
        删除订单
    destroy:
        订单详情
    """
    authentication_classes = (SessionAuthentication,JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated,)

    #序列化器
    # serializer_class = OrderInfoSerializer

    #添加订单详情信息
    def perform_create(self, serializer):
        #order订单表
        order = serializer.save()

        #清空购物车[object ]
        shop_cart = ShoppingCart.objects.filter(user=self.request.user)

        for shop in shop_cart:
            #生成订单详情
            order_goods = OrderGoods()
            order_goods.order = order
            order_goods.goods = shop.goods
            order_goods.goods_num = shop.goods_num
            order_goods.save()

            #清空购物车
            shop.delete()

        return order

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderInfoDetailSerializer
        else:
            return OrderInfoSerializer

    #获取当前用户的订单
    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)




from rest_framework.views import APIView
from rest_framework.response import Response
from utils.alipay import AliPay
from datetime import datetime
from mxshop1113.settings import private_key_path,ali_pub_key_path


class AlipayView(APIView):

    def get(self,request):
        """
        处理return_url
        :param request: 
        :return: 
        """
        #定义一个空的字典用来存储未加密的数据
        process_dict = {}

        #从get请求中获取参数
        for key,value in request.GET.items():
            process_dict[key] = value

        #取出sign
        sign = process_dict.pop("sign",None)

        #发送请求
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
        re_res = alipay.verify(process_dict, sign)

        #判断是否验签成功
        if re_res:
            #对订单做操作
            out_trade_no = process_dict.get("out_trade_no",None)
            #支付宝交易号
            trade_no = process_dict.get("trade_no",None)
            #交易状态
            pay_status = process_dict.get("trade_status","TRADE_SUCCESS")

            #通过订单号找到订单对象
            order_info = OrderInfo.objects.filter(order_sn=out_trade_no)
            for order in order_info:
                #通过订单找到商品  销量
                order_goods = order.order_goods.all()
                for order_god in order_goods:
                    goods = order_god.goods
                    goods.sold_num +=order_god.goods_num
                    goods.save()
                #order订单对象
                order.trade_no = trade_no
                order.pay_status = pay_status
                order.pay_time = datetime.now()
                order.save()

            #跳转到index页面
            res = redirect("index")
            res.set_cookie("nextPath","pay")
            return res

        else:
            #跳转到index页面
            res = redirect("index")
            return res


    def post(self,request):
        """
        处理notify_url
        :param request: 
        :return: 
        """
        #定义一个空的字典用来存储未加密的数据
        process_dict = {}

        #从get请求中获取参数
        for key,value in request.POST.items():
            process_dict[key] = value

        #取出sign
        sign = process_dict.pop("sign",None)

        #发送请求
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
        re_res = alipay.verify(process_dict, sign)

        #判断是否验签成功
        if re_res:
            #对订单做操作
            out_trade_no = process_dict.get("out_trade_no",None)
            #支付宝交易号
            trade_no = process_dict.get("trade_no",None)
            #交易状态
            pay_status = process_dict.get("trade_status",None)

            #通过订单号找到订单对象
            order_info = OrderInfo.objects.filter(order_sn=out_trade_no)
            for order in order_info:
                #通过订单找到商品  销量
                order_goods = order.order_goods.all()
                for order_god in order_goods:
                    goods = order_god.goods
                    goods.sold_num +=order_god.goods_num
                    goods.save()
                #order订单对象
                order.trade_no = trade_no
                order.pay_status = pay_status
                order.pay_time = datetime.now()
                order.save()



            return Response("success")




