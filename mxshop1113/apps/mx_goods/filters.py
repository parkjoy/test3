# coding=utf-8
#
from django_filters import rest_framework as filters
from mx_goods.models import Goods
from django.db.models import Q
# import rest_framework
class GoodsListFilter(filters.FilterSet):
    #字段名 field_name  150-200  大于150 小于200
    pricemin = filters.NumberFilter(field_name="shop_price", lookup_expr='gte',help_text="最低价格")
    pricemax = filters.NumberFilter(field_name="shop_price", lookup_expr='lte',help_text="最高价格")

    # Goods.objects.filter(shop_price__get=150)
    # Goods.objects.filter(shop_price__let=200)
    #模糊查询   sql  like
    # name = filters.CharFilter(field_name="name",lookup_expr="icontains")

    #通过指定的分类对象找到当前分类下面的所有商品  分类1 、2、3
    top_category = filters.NumberFilter(method="top_category_filters")

    #queryset 查询集商品数据   value传递过来的分类id
    def top_category_filters(self,queryset,name,value):
        return queryset.filter(Q(category_id=value)|Q(category__parent_category_id=value)|Q(category__parent_category__parent_category_id=value))


    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax',"top_category","is_hot","is_new"]