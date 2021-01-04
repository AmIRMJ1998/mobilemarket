from django.urls import path
from . import views

urlpatterns = [
    path('', views.blogIndex, name="blogIndex"),
    path('blog-post-slug/', views.blogPost, name="blogPost"),
]