from django.db import models
from django.contrib.auth.models import User # 引入 Django 自带的完美用户表

# 1. 分类表 (Category)
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="例如: 亚洲菜, 快餐, 咖啡厅")

    def __str__(self):
        return self.name

# 2. 餐厅表 (Restaurant)
class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    # 外键 (1:N 关系)：一个分类下有多个餐厅
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='restaurants')

    def __str__(self):
        return self.name

# 3. 评论表 (Review)
class Review(models.Model):
    # 外键 (1:N 关系)：一个餐厅有多个评论
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    # 外键 (1:N 关系)：一个用户可以发多条评论
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    rating = models.IntegerField(default=5, help_text="打分 1-5")
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # 自动记录发表时间

    def __str__(self):
        return f"{self.user.username} 评价了 {self.restaurant.name}"
