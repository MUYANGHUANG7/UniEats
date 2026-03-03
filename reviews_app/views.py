from django.shortcuts import render
from .models import Restaurant # 导入我们之前写的餐厅模型

def restaurant_list(request):
    # 1. 从数据库里把所有餐厅都捞出来
    restaurants = Restaurant.objects.all()
    
    # 2. 打包成一个字典准备发给前端
    context = {
        'restaurants': restaurants
    }
    
    # 3. 把数据交给 HTML 模板去渲染
    return render(request, 'reviews_app/restaurant_list.html', context)