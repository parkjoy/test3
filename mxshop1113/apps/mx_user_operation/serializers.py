# coding=utf-8
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from mx_user_operation.models import UserFav,UserLeavingMesage,UserAddress
from mx_goods.serializers import GoodsListSerializer


#会员中心收藏列表
class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsListSerializer()

    class Meta:
        #展示数据  get
        model = UserFav
        fields = ("goods","id")

#添加用户收藏
class UserFavSerializer(serializers.ModelSerializer):
    #找到当前登录用户  让用户的这个字段隐藏
    users = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        #展示数据  get
        model = UserFav
        fields = ("users","goods","id")

        #post  添加收藏商品
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('users', 'goods'),message="用户不可以重复收藏商品"
            )
        ]

#用户留言
class UserLeavingMesageSerializer(serializers.ModelSerializer):
    users = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True,format="%Y-%m-%d %H:%M")


    class Meta:
        model = UserLeavingMesage
        fields = ('users','message_type','subject','message','file','add_time','id')


#用户地址
class UserAddressSerializer(serializers.ModelSerializer):
    users = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True,format="%Y-%m-%d %H:%M")
    class Meta:
        model = UserAddress
        fields = ("users","province","city","district","address","signer_name","signer_mobile","add_time","id")