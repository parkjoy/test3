# coding=utf-8
import os
import sys

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+"../")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mxshop1113.settings")

import django
django.setup()

from mx_goods.models import Goods,GoodsImage,GoodsCategory
from db_tools.data.product_data import row_data


for goods_detail in row_data:
    #实例化商品对象
    goods = Goods()
    goods.name = goods_detail["name"]
    goods.goods_brief = goods_detail["desc"] if goods_detail["desc"] is not None else ""
    goods.goods_desc = goods_detail["goods_desc"] if goods_detail["goods_desc"] is not None else ""
    goods.maket_price = float(int(goods_detail["market_price"].replace("￥","").replace("元","")))
    goods.shop_price = float(int(goods_detail["sale_price"].replace("￥", "").replace("元", "")))
    goods.goods_front_image = goods_detail["images"][0] if goods_detail["images"] is not None else ""
    # goods.category

    #通过分类名找到分类对象
    category_name = goods_detail["categorys"][-1]
    categorys = GoodsCategory.objects.filter(name=category_name)
    if categorys:
        goods.category = categorys[0]

    goods.save()

    #保存当前商品的轮播图照片
    for image in goods_detail["images"]:
        goods_image = GoodsImage()
        goods_image.image = image
        goods_image.goods = goods
        goods_image.save()




