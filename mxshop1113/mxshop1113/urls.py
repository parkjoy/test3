"""mxshop1113 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
import xadmin
from mxshop1113.settings import MEDIA_ROOT
from django.views.static import serve
from mx_goods.views import GoodsListViewSet,GoodsCategoryViewset,HotSearchViewset,BannerViewset,IndexGoodsViewset
from mx_user.views import SendSmsViewset,UsersViewset
from mx_user_operation.views import UserFavViewset,UserLeavingMesageViewset,UserAddressViewset
from mx_trade.views import ShoppingCartViewset,OrderInfoViewset
from rest_framework.routers import DefaultRouter

#实例化路由对象
router = DefaultRouter()
#将列表页路径进行注册
router.register(r'goods', GoodsListViewSet,base_name="goods")
router.register(r'categorys',GoodsCategoryViewset,base_name="categorys")
router.register(r'code',SendSmsViewset,base_name="code")
router.register(r'users',UsersViewset,base_name="users")
router.register(r'hotsearchs',HotSearchViewset,base_name="hotsearchs")
router.register(r"userfavs",UserFavViewset,base_name="userfavs")
router.register(r"messages",UserLeavingMesageViewset,base_name="messages")
router.register(r"address",UserAddressViewset,base_name="address")
router.register(r"shopcarts",ShoppingCartViewset,base_name="shopcarts")
router.register(r'orders',OrderInfoViewset,base_name="orders")
router.register(r'banners',BannerViewset,base_name="banners")
router.register(r"indexgoods",IndexGoodsViewset,base_name="indexgoods")







from rest_framework_jwt.views import obtain_jwt_token
# from rest_framework.authtoken import views
from rest_framework.documentation import include_docs_urls
from mx_trade.views import AlipayView
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^docs/', include_docs_urls(title='慕学生鲜')),
	url(r'^media/(?P<path>.*)$',serve,{"document_root":MEDIA_ROOT}),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'', include(router.urls)),
    #用户初次登录的时候生成token，以后每一次登录都会对比token值
    # url(r'^api-token-auth/', views.obtain_auth_token),
    #jwt
    url(r'^login/$', obtain_jwt_token),
    #支付url
    url(r"^alipay/return/",AlipayView.as_view(),name="alipay"),
    #首页
    url(r'^index/$', TemplateView.as_view(template_name="index.html"), name="index"),
    url('', include('social_django.urls', namespace='social'))
]
