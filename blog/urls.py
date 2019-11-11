from django.urls import path
from .views import (
    all_posts_view, 
    single_post_view,
    category_view,
    search_posts_view,
    about_view
    )

urlpatterns = [
    path('', all_posts_view, name="all_posts_view"),
    path('<str:post_slug>/',single_post_view, name="single_post_view"),
    path('category/<str:category>/', category_view, name='category_view'),
    path('search', search_posts_view, name='search'),
    path('about', about_view),
]
