from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Avg, Count
from .models import Restaurant, Review, ReviewLike, Bookmark
from .forms import ReviewForm


def restaurant_list(request):
    # Performance: avoid N+1 queries in templates by preloading related category
    # and precomputing review_count/avg_rating in the database (single query).
    restaurants = (
        Restaurant.objects.select_related('category').annotate(
            avg_rating=Avg('reviews__rating'),
            review_count=Count('reviews', distinct=True),
        )
    )
    bookmarked_ids = set()
    if request.user.is_authenticated:
        bookmarked_ids = set(
            Bookmark.objects.filter(user=request.user).values_list('restaurant_id', flat=True)
        )
    context = {
        'restaurants': restaurants,
        'bookmarked_ids': bookmarked_ids,
    }
    return render(request, 'reviews_app/restaurant_list.html', context)


def restaurant_detail(request, restaurant_id):
    # Performance: fetch category and aggregate stats (average rating + review count)
    # in the same query used to load the restaurant.
    restaurant = get_object_or_404(
        Restaurant.objects.select_related('category').annotate(
            avg_rating=Avg('reviews__rating'),
            review_count=Count('reviews', distinct=True),
        ),
        id=restaurant_id,
    )

    # Performance: load review authors in the same query and precompute like counts
    # to prevent per-review COUNT(*) queries in the template.
    reviews = (
        Review.objects.filter(restaurant_id=restaurant_id)
        .select_related('user')
        .annotate(like_count=Count('likes', distinct=True))
        .order_by('-created_at')
    )

    is_bookmarked = False
    liked_review_ids = set()
    if request.user.is_authenticated:
        is_bookmarked = Bookmark.objects.filter(user=request.user, restaurant=restaurant).exists()
        # Performance: query liked review IDs in one shot (no need to iterate reviews).
        liked_review_ids = set(
            ReviewLike.objects.filter(user=request.user, review__restaurant_id=restaurant_id).values_list('review_id', flat=True)
        )

    context = {
        'restaurant': restaurant,
        'reviews': reviews,
        'is_bookmarked': is_bookmarked,
        'liked_review_ids': liked_review_ids,
    }
    return render(request, 'reviews_app/restaurant_detail.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('restaurant_list')
    else:
        form = UserCreationForm()

    return render(request, 'reviews_app/register.html', {'form': form})


@login_required
def add_review(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.restaurant = restaurant
            review.save()
            return redirect('restaurant_detail', restaurant_id=restaurant.id)
    else:
        form = ReviewForm()

    return render(request, 'reviews_app/add_review.html', {'form': form, 'restaurant': restaurant})


@login_required
def toggle_like(request, review_id):
    """AJAX endpoint: toggle like on a review, returns JSON."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    review = get_object_or_404(Review, id=review_id)
    like, created = ReviewLike.objects.get_or_create(user=request.user, review=review)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({'liked': liked, 'count': review.likes.count()})


@login_required
def toggle_bookmark(request, restaurant_id):
    """AJAX endpoint: toggle bookmark on a restaurant, returns JSON."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, restaurant=restaurant)

    if not created:
        bookmark.delete()
        bookmarked = False
    else:
        bookmarked = True

    return JsonResponse({'bookmarked': bookmarked})
