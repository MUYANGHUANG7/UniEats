from django.test import TestCase
from django.contrib.auth.models import User
from .models import Category, Restaurant, Review

class UniEatsTests(TestCase):
    def setUp(self):
        # 1. 准备工作：机器人在虚拟数据库里造一些假数据
        self.user = User.objects.create_user(username='testboy', password='password123')
        self.category = Category.objects.create(name='Test Category')
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            address='123 Test Street',
            category=self.category
        )
        self.review = Review.objects.create(
            restaurant=self.restaurant,
            user=self.user,
            rating=5,
            comment='Super delicious!'
        )

    def test_models_creation(self):
        # 2. 测试一：检查数据库模型是不是真的建成功了
        self.assertEqual(self.category.name, 'Test Category')
        self.assertEqual(self.restaurant.category.name, 'Test Category')
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.user.username, 'testboy')

    def test_homepage_view(self):
        # 3. 测试二：模拟浏览器访问主页，看看会不会崩溃
        response = self.client.get('/')
        # 200 代表 HTTP 成功状态码，说明网页正常打开了
        self.assertEqual(response.status_code, 200) 
        # 检查网页的 HTML 代码里，有没有包含我们刚才建的餐厅名字
        self.assertContains(response, 'Test Restaurant')
