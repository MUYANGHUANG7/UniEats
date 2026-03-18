from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
import json
from .models import Category, Restaurant, Review, ReviewLike, Bookmark


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

    def test_toggle_like_requires_login(self):
        url = reverse('toggle_like', args=[self.review.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

    def test_toggle_like_endpoint_authenticated(self):
        self.client.login(username='testboy', password='password123')
        url = reverse('toggle_like', args=[self.review.id])

        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['liked'], True)
        self.assertEqual(data['count'], 1)
        self.assertEqual(ReviewLike.objects.filter(user=self.user, review=self.review).count(), 1)

        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['liked'], False)
        self.assertEqual(data['count'], 0)
        self.assertEqual(ReviewLike.objects.filter(user=self.user, review=self.review).count(), 0)

    def test_toggle_bookmark_endpoint_authenticated(self):
        self.client.login(username='testboy', password='password123')
        url = reverse('toggle_bookmark', args=[self.restaurant.id])

        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['bookmarked'], True)
        self.assertEqual(Bookmark.objects.filter(user=self.user, restaurant=self.restaurant).count(), 1)

        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['bookmarked'], False)
        self.assertEqual(Bookmark.objects.filter(user=self.user, restaurant=self.restaurant).count(), 0)
