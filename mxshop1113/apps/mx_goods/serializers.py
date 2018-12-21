# coding=utf-8
from rest_framework import serializers
from mx_goods.models import Goods,GoodsCategory,GoodsImage,HotSearch,Banner,IndexAd,GoodsCategoryBrand
from django.db.models import Q


#三级类
class GoodsCategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"


#二级类
class GoodsCategorySerializer2(serializers.ModelSerializer):
    #三级类
    sub_cat = GoodsCategorySerializer3(many=True)
    class Meta:
        model = GoodsCategory
        fields = "__all__"


#一级类
class GoodsCategorySerializer(serializers.ModelSerializer):
    #二级类
    sub_cat = GoodsCategorySerializer2(many=True)
    class Meta:
        model = GoodsCategory
        fields = "__all__"


#轮播图序列化器
class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ("image",)


#list get 输出
class GoodsListSerializer(serializers.ModelSerializer):
    #嵌套序列化输出
    category = GoodsCategorySerializer()
    #分类id ---> 分类对象----> 序列化 ----->  赋值  category
    good_images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        fields = "__all__"


#热搜
class HotSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotSearch
        fields = ("keywords",)


#轮播图
class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"


#商家
class GoodsCategoryBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategoryBrand
        fields = "__all__"


#首页分类
class IndexGoodsSerializer(serializers.ModelSerializer):
    #二级类
    sub_cat = GoodsCategorySerializer2(many=True)
    #商家ser.data
    brands = GoodsCategoryBrandSerializer(many=True)
    #当前分类下的商品
    goods = serializers.SerializerMethodField()
    #当前分类下的广告商品
    ad_goods = serializers.SerializerMethodField()


    def get_goods(self, obj):
        #通过分类的id找到当前分类的下的所有商品
        goods_info = Goods.objects.filter(Q(category_id=obj.id)|Q(category__parent_category_id=obj.id)|Q(category__parent_category__parent_category_id=obj.id))
        #[<object>,<obj>] serialzrobj.data
        good_serializer = GoodsListSerializer(goods_info,many=True,context={"request":self.context["request"]}).data
        return good_serializer

    def get_ad_goods(self,obj):
        #通过分类的id找到当前分类下面的广告商品
        index_info = IndexAd.objects.filter(category_id=obj.id)
        if index_info:
            #找到商品对象
            goods_info = index_info[0].goods
            #序列化
            good_serializer = GoodsListSerializer(goods_info, many=False,context={"request":self.context["request"]}).data
            return good_serializer

    class Meta:
        model = GoodsCategory
        fields = "__all__"

