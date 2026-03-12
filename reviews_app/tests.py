from django.test import TestCase
from django.contrib.auth.models import User
from .models import Category, Restaurant, Review


class UniEatsTests(TestCase):
    def setUp(self):
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
        self.assertEqual(self.category.name, 'Test Category')
        self.assertEqual(self.restaurant.category.name, 'Test Category')
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.user.username, 'testboy')

    def test_homepage_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Restaurant')
