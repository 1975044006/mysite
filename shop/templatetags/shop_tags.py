from django import template
from shop.models import *

register = template.Library()


@register.simple_tag
def k2v(k, dict1: dict):
    return dict1.get(k)


@register.filter(name="rest")
def replacestr(value: str, str1):
    return value.replace("ha", str1)


@register.filter(name="good2p")
def good2price(goodsname):
    return Goods.objects.get(goodsName=goodsname).price

@register.filter
def totalprice(price,num):
    return price*num

@register.filter
def datetime2str(date):
    print(date)
    return date.strftime("%Y-%m-%d %H:%M:%S")

@register.filter
def filterk2v(dictt: dict, k):
    return dictt.get(k)

@register.filter
def browsuser(userName):
    if userName is None:
        return "未登录"
    else:
        return userName.userName

@register.filter
def getordertime(orderqueryset):
    return orderqueryset[0].time

@register.filter
def getitems(dictt:dict):
    return dictt.items()

