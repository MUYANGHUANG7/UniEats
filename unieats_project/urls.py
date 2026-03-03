from django.contrib import admin
from django.urls import path, include # 注意这里多导入了一个 include

urlpatterns = [
    path('admin/', admin.site.urls),
    # 这句话的意思是：剩下的所有网址，都交给 reviews_app 自己去处理
    path('', include('reviews_app.urls')), 
]