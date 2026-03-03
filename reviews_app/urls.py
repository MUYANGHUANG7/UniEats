from django.urls import path
from django.contrib.auth import views as auth_views # 引入 Django 自带的 Auth 视图
from . import views

urlpatterns = [
    # 主页
    path('', views.restaurant_list, name='restaurant_list'),
    
    # 认证相关的三个网址
    path('register/', views.register, name='register'),
    # 使用 Django 自带的 LoginView，并告诉它去找哪个 HTML 文件
    path('login/', auth_views.LoginView.as_view(template_name='reviews_app/login.html'), name='login'),
    # 使用 Django 自带的 LogoutView
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # 网址里带上餐厅的 id，这样我们就知道用户在评哪家店
    path('restaurant/<int:restaurant_id>/add_review/', views.add_review, name='add_review'),
]