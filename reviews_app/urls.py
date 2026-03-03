from django.urls import path
from . import views

urlpatterns = [
    # 当用户访问主页（空网址）时，调用 views 里的 restaurant_list 函数
    path('', views.restaurant_list, name='restaurant_list'),
]