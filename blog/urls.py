from django.urls import path
from blog.views import views, ajaxviews

app_name = 'blog'

urlpatterns = [
    path('', views.blogindex, name = "blog_index"),
    path('<slug:slug>/', views.blogPost, name = "blog_post"),
    # comment ajax function path
    path('<slug:slug>/comment/add/', ajaxviews.add_new_comment, name = "alax_add_new_comment")
]