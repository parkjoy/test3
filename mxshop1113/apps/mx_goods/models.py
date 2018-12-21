from django.db import models
from datetime import datetime
from DjangoUeditor.models import UEditorField
# Create your models here.

class GoodsCategory(models.Model):
    """
    商品类别
    """
    CATEGORY_TYPE = (
        (1,"一级类目"),
        (2, "二级类目"),
        (3, "三级类目")
    )
    name = models.CharField(max_length=30,default="",verbose_name="分类名",help_text="分类名")
    code = models.CharField(default="",max_length=30,verbose_name="分类编号")
    desc = models.CharField(default="",max_length=100,verbose_name="分类描述")
    category_type = models.CharField(max_length=100,verbose_name="分类所属级别",choices=CATEGORY_TYPE)
    #因为一级分类没有父类  所以需要设置默认值
    parent_category = models.ForeignKey("self",verbose_name="当前分类的父类",null=True,blank=True,related_name="sub_cat")
    is_table = models.BooleanField(default=False,verbose_name="是否在导航栏")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "商品类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class GoodsCategoryBrand(models.Model):
    """
    品牌
    """
    #只有一级分类下有品牌商
    category = models.ForeignKey(GoodsCategory,verbose_name="所属分类",related_name="brands",null=True,blank=True)
    name = models.CharField(default="",max_length=40,verbose_name="品牌名")
    desc = models.CharField(default="",max_length=100,verbose_name="品牌简介")
    image = models.ImageField(upload_to="brands/",max_length=200)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "品牌"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Goods(models.Model):
    """
    商品
    """
    category = models.ForeignKey(GoodsCategory,verbose_name="商品所在类别")
    goods_sn = models.CharField(max_length=30,default="",verbose_name="商品货号")
    name = models.CharField(max_length=60,verbose_name="商品名")
    click_num = models.IntegerField(default=0,verbose_name="点击量")
    sold_num = models.IntegerField(default=0,verbose_name="销售量")
    fav_num = models.IntegerField(default=0,verbose_name="收藏量")
    goods_num = models.IntegerField(default=0,verbose_name="库存量")
    maket_price = models.FloatField(default=0,verbose_name="市场价")
    shop_price = models.FloatField(default=0,verbose_name="本店价")
    goods_brief = models.TextField(max_length=500,verbose_name="商品简短简介")
    goods_desc = UEditorField(verbose_name="内容",imagePath="goods/desc/",filePath="goods/files/",
                              width=1000,
                              height=300,default=""
                              )
    ship_free = models.BooleanField(default=False,verbose_name="是否承担运费")
    goods_front_image = models.ImageField(max_length=100,upload_to="goods/images/",verbose_name="商品封面图",null=True,blank=True)
    is_new = models.BooleanField(default=False,verbose_name="是否新品")
    is_hot = models.BooleanField(default=False,verbose_name="是否热卖")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class GoodsImage(models.Model):
    """
    商品详细页轮播图
    """
    goods = models.ForeignKey(Goods,verbose_name="商品",related_name="good_images")
    image = models.ImageField(upload_to="goods/lun/images/",max_length=200,verbose_name="图片")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "商品详细页轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name

class Banner(models.Model):
    """
    首页轮播图
    """
    goods = models.ForeignKey(Goods, verbose_name="商品", related_name="banner")
    image = models.ImageField(upload_to="goods/banner/images",max_length=200, verbose_name="图片")
    index = models.IntegerField(default=0,verbose_name="轮播顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "首页轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name

class HotSearch(models.Model):
    """
    热搜词
    """
    keywords = models.CharField(max_length=50,verbose_name="热搜词",default="")
    index = models.IntegerField(default=0, verbose_name="显示顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "热搜词"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.keywords

class IndexAd(models.Model):
    """
    首页分类广告
    """
    category = models.ForeignKey(GoodsCategory,verbose_name="商品所在类别",related_name="category")
    goods = models.ForeignKey(Goods,verbose_name="商品",related_name="goods")

    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "首页分类广告"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.category.name
