from django.urls import path
from blog.views import views, ajaxviews

app_name = 'blog'

urlpatterns = [
    path('', views.blogindex, name = "blog_index"),
    path('<slug:slug>/', views.blogPost, name = "blog_post"),
    # comment ajax function path
    path('post/comment/add/', ajaxviews.add_new_comment, name = "ajax_add_new_comment"),
    path('post/comment/reply/', ajaxviews.replyComment, name = "replyComment"),
    path('post/comment/like_or_dislike_comment/', ajaxviews.like_or_dislike_comment, name = "like_or_dislike_comment"),


    path('post/rate/add/', ajaxviews.add_point_in_post, name = "add_point_in_post"),
]