from django.contrib import admin
from .models import Category, Restaurant, Review

# 把这三张表注册到后台
admin.site.register(Category)
admin.site.register(Restaurant)
admin.site.register(Review)