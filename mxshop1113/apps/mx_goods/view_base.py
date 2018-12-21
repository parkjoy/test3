from mx_goods.models import Goods
from django.views.generic import View
from django.http import JsonResponse,HttpResponse
from django.forms.models import model_to_dict
from django.core import serializers

class GoodsListView(View):
    def get(self,request):
        #获取部分商品
        goods_list = Goods.objects.all()[:10]
        json_data = serializers.serialize("json",goods_list)

        #新建一个空列表
        # goods_new_list = []
        # for good in goods_list:
            # goods_dict = {}
            # goods_dict["name"] = good.name
            # goods_dict["shop_price"] = good.shop_price
            # goods_dict["add_time"] = good.add_time
            # goods_new_list.append(goods_dict)
        #     json_dict = model_to_dict(good)
        #     goods_new_list.append(json_dict)
        #
        # import json
        # goods_new_list = json.loads(json_data)
        # return JsonResponse(goods_new_list,safe=False)
        return HttpResponse(json_data,content_type="application/json")




