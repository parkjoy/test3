# coding=utf-8
import os
import sys
#获取当前脚本的路径
pwd = os.path.dirname(os.path.realpath(__file__))
#将项目目录添加到解释器环境中
sys.path.append(pwd+"../")


#需要单独使用django的model  需要配置django  model环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mxshop1113.settings")

#使用django 并且初始化
import django
django.setup()


#这里开始导入数据
from mx_goods.models import GoodsCategory
from db_tools.data.category_data import row_data

for lev1_cat in row_data:
    #实例化分类对象  一级类目
    lev1_intance = GoodsCategory()
    lev1_intance.name = lev1_cat["name"]
    lev1_intance.code = lev1_cat["code"]
    lev1_intance.category_type = 1
    lev1_intance.save()

    #二级类目
    for lev2_cat in lev1_cat["sub_categorys"]:
        lev2_intance = GoodsCategory()
        lev2_intance.name = lev2_cat["name"]
        lev2_intance.code = lev2_cat["code"]
        lev2_intance.category_type = 2
        lev2_intance.parent_category = lev1_intance
        lev2_intance.save()

        # 三级类目
        for lev3_cat in lev2_cat["sub_categorys"]:
            lev3_intance = GoodsCategory()
            lev3_intance.name = lev3_cat["name"]
            lev3_intance.code = lev3_cat["code"]
            lev3_intance.category_type = 3
            lev3_intance.parent_category = lev2_intance
            lev3_intance.save()
















