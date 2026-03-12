#!/usr/bin/env python
"""
Populate database with sample restaurant data
Run this script with: python populate_data.py
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unieats_project.settings')
django.setup()

from reviews_app.models import Category, Restaurant

def populate():
    """Populate the database with sample data"""

    print("🍽️  Starting to populate database with sample data...")

    # Create categories
    categories_data = [
        "Chinese",
        "Italian",
        "Fast Food",
        "Cafe",
        "Japanese",
        "Mexican",
    ]

    print("\n📁 Creating categories...")
    categories = {}
    for cat_name in categories_data:
        category, created = Category.objects.get_or_create(name=cat_name)
        categories[cat_name] = category
        if created:
            print(f"  ✅ Created category: {cat_name}")
        else:
            print(f"  ℹ️  Category already exists: {cat_name}")

    # Create restaurants
    restaurants_data = [
        {
            "name": "Dragon Wok",
            "address": "123 University Ave, Campus Center",
            "description": "Authentic Chinese cuisine with a modern twist. Popular dishes include Kung Pao Chicken and Mapo Tofu.",
            "category": "Chinese"
        },
        {
            "name": "Bella Pasta",
            "address": "456 College Street, Near Library",
            "description": "Italian restaurant specializing in fresh pasta and wood-fired pizzas.",
            "category": "Italian"
        },
        {
            "name": "Quick Burger",
            "address": "789 Student Union Building",
            "description": "Fast food joint offering burgers, fries, and shakes. Quick service for busy students.",
            "category": "Fast Food"
        },
        {
            "name": "Campus Cafe",
            "address": "321 Main Hall, Ground Floor",
            "description": "Cozy cafe serving coffee, sandwiches, and pastries. Great study spot with free WiFi.",
            "category": "Cafe"
        },
        {
            "name": "Sakura Sushi",
            "address": "555 East Campus Road",
            "description": "Fresh sushi and Japanese cuisine. Try their signature dragon roll and miso ramen.",
            "category": "Japanese"
        },
        {
            "name": "Taco Fiesta",
            "address": "888 West Campus Plaza",
            "description": "Vibrant Mexican restaurant with tacos, burritos, and quesadillas. Vegetarian options available.",
            "category": "Mexican"
        },
        {
            "name": "Green Leaf Cafe",
            "address": "111 Science Building",
            "description": "Healthy cafe focusing on salads, smoothies, and organic meals. Perfect for health-conscious students.",
            "category": "Cafe"
        },
        {
            "name": "Pizza Paradise",
            "address": "222 Dormitory Complex",
            "description": "New York style pizza by the slice. Late night delivery available for students.",
            "category": "Italian"
        },
    ]

    print("\n🏪 Creating restaurants...")
    for rest_data in restaurants_data:
        category = categories[rest_data["category"]]
        restaurant, created = Restaurant.objects.get_or_create(
            name=rest_data["name"],
            defaults={
                "address": rest_data["address"],
                "description": rest_data["description"],
                "category": category
            }
        )
        if created:
            print(f"  ✅ Created restaurant: {rest_data['name']} ({rest_data['category']})")
        else:
            print(f"  ℹ️  Restaurant already exists: {rest_data['name']}")

    print("\n" + "="*60)
    print("✨ Database population completed!")
    print(f"📊 Total categories: {Category.objects.count()}")
    print(f"📊 Total restaurants: {Restaurant.objects.count()}")
    print("="*60)
    print("\n💡 You can now:")
    print("   1. Visit the homepage to see all restaurants")
    print("   2. Register/login to write reviews")
    print("   3. Use Django admin to manage data: python manage.py createsuperuser")
    print()

if __name__ == '__main__':
    populate()
