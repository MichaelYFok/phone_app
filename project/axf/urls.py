# -*- coding:utf-8 -*-
from django.conf.urls import url
from axf import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^home/$', views.home),
    url(r'^market/(\w+)/(\w+)/(\w+)/$', views.market),


    url(r'^cart/$', views.cart),
    #修改购物车
    url(r'^carts/$', views.carts),
    #下订单
    url(r'^order/$', views.order),



    url(r'^mine/$', views.mine),
    # 登录
    url(r'^login/$', views.login),
    # 发送验证码
    url(r'verifycode/$', views.verifycode),
    # 退出
    url(r'quit/$', views.quit),
]