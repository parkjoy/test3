from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from mx_user_operation.models import UserFav,UserLeavingMesage,UserAddress
from mx_user_operation.serializers import UserFavSerializer,UserFavDetailSerializer,UserLeavingMesageSerializer,UserAddressSerializer
from utils.permission import IsOwnerOrReadOnly

class UserFavViewset(viewsets.GenericViewSet,mixins.CreateModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
    """
    list:
        收藏列表
    create:
        添加收藏
    retrieve:
        查看收藏的某一个商品
    destroy:
        取消收藏
    """
    #获取用户收藏列表
    queryset = UserFav.objects.all()
    #指定序列化器
    serializer_class = UserFavSerializer
    #权限
    permission_classes = (permissions.IsAuthenticated,IsOwnerOrReadOnly)
    #认证
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)

    lookup_field = "goods_id"

    # 收藏+1
    # def perform_create(self, serializer):
    #     ins = serializer.save()
    #     ins.goods.fav_num +=1
    #     ins.goods.save()


    #收藏-1
    # def perform_destroy(self, instance):
    #     instance.goods.fav_num -=1
    #     instance.goods.save()
    #     instance.delete()



    def get_serializer_class(self):
        if self.action == "create":
            return UserFavSerializer
        elif self.action == "list":
            return UserFavDetailSerializer
        return UserFavSerializer

    def get_queryset(self):
        #过滤  当前登录的用户
        return UserFav.objects.filter(users=self.request.user)

class UserLeavingMesageViewset(viewsets.GenericViewSet,mixins.CreateModelMixin,mixins.ListModelMixin,mixins.DestroyModelMixin):
    """
    list:
        留言列表
    create:
        添加留言
    destroy:
        删除留言
    """
    #权限
    permission_classes = (permissions.IsAuthenticated,IsOwnerOrReadOnly)
    #认证
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)
    #查询集
    queryset = UserLeavingMesage.objects.all()
    #序列化器
    serializer_class = UserLeavingMesageSerializer



    #获取当前登录的用户留言
    def get_queryset(self):
        return UserLeavingMesage.objects.filter(users=self.request.user)

class UserAddressViewset(viewsets.ModelViewSet):
    """
    list:
        地址列表
    create:
        添加地址
    destroy:
        删除地址
    """
    #权限
    permission_classes = (permissions.IsAuthenticated,IsOwnerOrReadOnly)
    #认证
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer

    def get_queryset(self):
        return UserAddress.objects.filter(users=self.request.user)
