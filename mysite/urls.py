"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from shop import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('login/', views.login, name="login"),
    path('register/', views.register),
    path('sendcode/', views.sendcode),
    path('testcookies/', views.testcookies),
    path('logout/', views.logout),
    path('upload/', views.upload),
    path('showphoto/', views.showphoto),
    path('modgood/', views.modgood),
    path('delgood/', views.delgood),
    path('buylog/', views.buylog),
    path('browsinglog/', views.browsinglog),
    path('addgood/', views.addgood),
    path('gooddetail/', views.gooddetail),
    path('shopcart/', views.shopCart),
    path('settlecart/', views.settlecart),
    path('delshopcart/', views.delshopcart),
    path('usercenter/', views.usercenter),
    path('manageseller/', views.manageseller),
    path('memberupd/', views.memberupd),
    path('addmember/', views.addmember),
    path('delmember/', views.delmember),
    path('sellinfo/', views.sellinfo),
    path('sellerPERF/', views.sellerPERF),
    path('browsehistory/', views.browsehistory),
    path('userbuylog/', views.userbuylog),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
