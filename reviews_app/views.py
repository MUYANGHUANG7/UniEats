from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Restaurant
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required # 引入防偷窥保安
from .models import Restaurant, Review
from .forms import ReviewForm

# 1. 餐厅列表视图 (你之前写的，保持不变)
def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    context = {'restaurants': restaurants}
    return render(request, 'reviews_app/restaurant_list.html', context)

# 2. 新增：用户注册视图
def register(request):
    # 如果用户是点击了“提交”按钮发来的数据
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() # 保存新用户到数据库
            login(request, user) # 注册成功后自动帮他登录
            return redirect('restaurant_list') # 跳转回主页
    else:
        # 如果用户只是刚打开注册页面，给他一个空表单
        form = UserCreationForm()
        
    return render(request, 'reviews_app/register.html', {'form': form})

# 加上这个装饰器，强制要求必须登录才能访问这个视图
@login_required 
def add_review(request, restaurant_id):
    # 根据网址里的 id 找到是哪家餐厅
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False) # 先别急着存数据库，我还要加点料
            review.user = request.user # 把当前登录的用户绑上去
            review.restaurant = restaurant # 把当前餐厅绑上去
            review.save() # 资料齐全，正式保存！
            return redirect('restaurant_list') # 跳回主页
    else:
        form = ReviewForm()
        
    return render(request, 'reviews_app/add_review.html', {'form': form, 'restaurant': restaurant})