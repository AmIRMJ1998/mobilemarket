from django.urls import path
from . import views

app_name = 'market'

urlpatterns = [
    path('', views.index, name="index"),
    # path('products/', views.products, name="products"),
    path('products/mobile', views.mobile, name="mobile"),
    # path('products/tablet', views.tablet, name="tablet"),

    path('products/mobile/<slug:Slug>', views.product, name="product"),
    path('products/rate/mobile/', views.rate, name="Rate"),
    path('products/comment/mobile/', views.createComment, name="createComment"),
    path('products/comment/like/mobile/', views.likeComment, name="likeComment"),
    path('products/comment/reply/mobile/', views.replyComment, name="replyComment"),
    

    path('card/', views.card, name="card"),
    path('register/', views.register, name="register"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('dashboard/orders', views.orders, name="orders"),
    path('dashboard/orders/order', views.order, name="order"),

    path('dashboard/information', views.information, name="information"),
    path('dashboard/information/change', views.changeInformation, name="changeInformation"),

    path('dashboard/favorites', views.favorites, name="favorites"),
    path('dashboard/favorites/addtofavorite', views.addtofavorite, name="addtofavorite"),

    path('dashboard/messages', views.messages, name="messages"),
    path('dashboard/messages/<int:id>', views.message, name="message"),
    path('dashboard/seen/message', views.changeMessageStatus, name="changeMessageStatus"),

    path('dashboard/comments', views.comments, name="comments"),

    path('compare/', views.compare, name="compare"),
    path('compare/mobiles-by-brand', views.findMobileByBrand, name="findMobileByBrand"),
    path('compare/add-to-compare', views.addToCompare, name="addToCompare"),
    path('compare/do-compare', views.doCompare, name="doCompare"),

    path('contact-us/', views.contactUs, name="contact-us"),
    path('rules/', views.rules, name="rules"),
    path('login/', views.loginPage, name='login'),

    path('last-comments/', views.lastComments, name="lastComments"),

    path('loginRequest/', views.loginRequest, name='loginRequest'),
    path('logout/', views.logoutRequest, name='logoutRequest')
]