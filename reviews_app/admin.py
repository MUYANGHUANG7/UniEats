from django.contrib import admin
from .models import Category, Restaurant, Review, ReviewLike, Bookmark

admin.site.register(Category)
admin.site.register(Restaurant)
admin.site.register(Review)
admin.site.register(ReviewLike)
admin.site.register(Bookmark)
