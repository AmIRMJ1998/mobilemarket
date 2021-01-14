from django.urls import path
from . import views

app_name = 'market'

urlpatterns = [
    path('', views.index, name="index"),
    path('products/', views.products, name="products"),
    path('products/mobile', views.mobile, name="mobile"),
    path('products/tablet', views.tablet, name="tablet"),
    path('products/mobile/<slug:slug>', views.product, name="product"),
    path('card/', views.card, name="card"),
    path('register/', views.register, name="register"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('dashboard/orders', views.orders, name="orders"),
    path('dashboard/orders/order', views.order, name="order"),
    path('dashboard/information', views.information, name="information"),
    path('dashboard/favorites', views.favorites, name="favorites"),
    path('dashboard/messages', views.messages, name="messages"),
    path('dashboard/messages/message-slug', views.message, name="message"),
    path('dashboard/comments', views.comments, name="comments"),
    path('compare/', views.compare, name="compare"),
    path('contact-us/', views.contactUs, name="contact-us"),
    path('login/', views.loginPage, name='login'),


    path('loginRequest/', views.loginRequest, name='loginRequest'),
    path('logout/', views.logoutRequest, name='logoutRequest')
]