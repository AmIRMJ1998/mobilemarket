from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import User, UserManager, Mobile, Comment, Contact, Message, Slider, Factor
from blog.models import Post

User = get_user_model()
# Main Section Title
admin.site.site_header = 'Mobile Market'
# --------------------------------
# Post Admin Section
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','points','createdate','publishdate')
    search_fields = ['title', 'slug', 'text']
    list_filter = ('publish',)
    ordering = ['id', 'createdate']
# Mobile Admin Section
@admin.register(Mobile)
class MobileAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'price', 'points', 'inventory')
    search_fields = ['title', 'slug', 'brand', 'description']
    list_filter = ('publish',)
    ordering = ['id', 'datecreate']
# Contact Admin Section
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('title', 'mobilenumber', 'email', 'createdate', 'status')
    search_fields = ['title', 'mobilenumber', 'email', 'description']
    list_filter = ('status',)
    ordering = ['id', 'createdate']
# Comment Admin Section
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'FK_User', 'datecreate')
    search_fields = ['description', 'FK_User']
    ordering = ['id', 'datecreate']
# Message Admin Section
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'datetime',)
    search_fields = ['title', 'text']
    ordering = ['id', 'datetime']
# Slider Admin Section
@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('description', 'link', 'publish')
    search_fields = ['description', 'link']
    list_filter = ('publish',)
    ordering = ['id']
# Factor Admin Section
@admin.register(Factor)
class FactorAdmin(admin.ModelAdmin):
    list_display = ('number', 'FK_User', 'total_price', 'payment_status', 'status', 'orderdate')
    search_fields = ['number', 'FK_User']
    list_filter = ('payment_status', 'status')
    ordering = ['id', 'orderdate']
# User Admin Section
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username','first_name','last_name','mobile','email','active','superuser','staff')
    search_fields = ['username','first_name','last_name','mobile','email']
    list_filter = ('active','superuser','staff')
    ordering = ['id']
admin.site.register = (User, UserAdmin)
admin.site.register = (UserManager)