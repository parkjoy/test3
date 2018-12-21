from django.shortcuts import render

# Create your views here.
from mx_goods.models import Goods,GoodsCategory,HotSearch,Banner
from mx_goods.serializers import GoodsListSerializer,GoodsCategorySerializer,HotSearchSerializer,BannerSerializer,IndexGoodsSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from mx_goods.filters import GoodsListFilter
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework.throttling import AnonRateThrottle,UserRateThrottle

#列表页分页
class GoodsListPagination(PageNumberPagination):
    # 页数关键字名，默认为
    page_query_param = "page"
    # get_page_sizes=30
    # 每一页要取多少条数据的参数，默认为None
    page_size_query_param = "get_page_sizes"
    # 前端最多能设置的每页数量
    max_page_size = 50
    # 每一页显示的条数
    page_size = 12

#列表页接口
class GoodsListViewSet(CacheResponseMixin,viewsets.GenericViewSet,mixins.ListModelMixin,mixins.RetrieveModelMixin):
    """
    list:
        商品列表
    retrieve:
        商品详情
    """
    #指定查询集
    queryset = Goods.objects.all()
    #指定序列化器
    serializer_class = GoodsListSerializer
    #指定的认证器类
    # authentication_classes = (TokenAuthentication,)
    #指定自定义分页
    pagination_class = GoodsListPagination
    #搜索  排序  过滤
    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter)
    #自定义过滤器
    filterset_class = GoodsListFilter
    #搜索
    search_fields = ('name', 'goods_brief',"goods_desc")
    #排序
    ordering_fields = ('shop_price', 'sold_num')

    #限速
    throttle_classes = (UserRateThrottle,AnonRateThrottle)

    #用户点击商品，商品的点击量+1
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num +=1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

#分类接口
class GoodsCategoryViewset(CacheResponseMixin,viewsets.GenericViewSet,mixins.ListModelMixin,mixins.RetrieveModelMixin):
    """
    list:
        分类列表
    retrieve:
        分类详情
    """
    #查询集
    queryset = GoodsCategory.objects.filter(category_type=1)
    #指定序列化器
    serializer_class = GoodsCategorySerializer

#热搜
class HotSearchViewset(viewsets.GenericViewSet,mixins.ListModelMixin):
    queryset = HotSearch.objects.all().order_by("-index")[:5]
    serializer_class = HotSearchSerializer

#轮播图
class BannerViewset(viewsets.GenericViewSet,mixins.ListModelMixin):
    queryset = Banner.objects.all().order_by("index")[:3]
    serializer_class = BannerSerializer


#首页分类
class IndexGoodsViewset(viewsets.GenericViewSet,mixins.ListModelMixin):
    #找分类
    queryset = GoodsCategory.objects.filter(is_table=True,name__in=["生鲜食品","酒水饮料"])
    #序列化
    serializer_class = IndexGoodsSerializer



