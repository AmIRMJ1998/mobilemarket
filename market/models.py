from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.postgres.fields import ArrayField
from django.db.models import JSONField
from datetime import datetime
from django.db import models
import os

# --------------------------------------------------------------------------------------------------------------------------------------

class UserManager(BaseUserManager):
    def create_user(self, username, email = None, nationalcode = None, password = None, **kwargs):
        if not username:
            raise ValueError("Users must have username")
        if not password:
            raise ValueError("Users must have password")
        if not email:
            raise ValueError("Users must have email")
        if not nationalcode:
            raise ValueError("Users must have nationalcode")
        user = self.model(username = username, **kwargs)
        user.email = email
        user.nationalcode = nationalcode
        user.set_password(password)
        user.save()
        return user

    
    def create_staffuser(self, username, email = None, nationalcode = None, password = None, **kwargs):
        user = self.model(username = username, staff = True, **kwargs)
        user.email = email
        user.nationalcode = nationalcode
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, username, email = None, nationalcode = None, password = None, **kwargs):
        user = self.model(username = username, staff = True, superuser = True, **kwargs)
        user.email = email
        user.nationalcode = nationalcode
        user.set_password(password)
        user.save()
        return user
        
# --------------------------------------------------------------------------------------------------------------------------------------

# User (کاربر) Model
class User (AbstractBaseUser):
    first_name = models.CharField(verbose_name = 'first name', max_length = 150)
    last_name = models.CharField(verbose_name = 'last name', max_length = 300)
    username = models.CharField(verbose_name = 'username', max_length = 255, unique = True)
    mobile = models.CharField(verbose_name = 'mobile number', max_length = 11, unique = True, blank = True, null = True)
    email = models.EmailField(verbose_name = 'email', unique = True, null = True)
    nationalcode = models.CharField(verbose_name = 'national code', max_length = 10, blank = True, null = True)
    address = models.JSONField(verbose_name = 'آدرس', blank = True, null = True)
    active = models.BooleanField(verbose_name = 'وضعیت فعالیت', default = True)
    superuser = models.BooleanField(verbose_name = 'وضعیت مدیریت', default = False)
    staff = models.BooleanField(verbose_name = 'وضعیت کارمندی', default = False)
    citypercode = models.CharField(verbose_name = 'پیش شماره', max_length = 3, blank = True, null = True)
    phone = models.CharField(verbose_name = 'شماره تلفن ثابت', max_length = 8, blank = True)
    brithday = models.DateField(verbose_name = 'تاریخ تولد', null = True, auto_now_add = True)
    comment_list = models.JSONField(verbose_name = 'لیست نظرات ها', null = True, blank = True)
    factor_list = models.JSONField(verbose_name = 'لیست فاکتور ها', null = True, blank = True)
    message_list = JSONField(verbose_name = 'لیست پیام ها', null = True, blank = True)
    favorite_list = JSONField(verbose_name = 'لیست موقعیت های مورد علاقه', null = True, blank = True)
    createdate = models.DateTimeField(verbose_name = 'تاریخ عضویت', auto_now_add = True)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email', 'nationalcode']

    objects = UserManager()

    @property
    def is_active(self):
        return self.active

    @property
    def is_superuser(self):
        return self.superuser

    @property
    def is_staff(self):
        return self.staff

    def __str__(self):
       return "{}".format(self.username)

    def has_perm(self, perm, obj = None):
        return True

    def has_module_perms(self, app_label):
        return True

    # get user full name
    def get_fullname(self):
        return ' '.join([self.first_name, self.last_name])

    # address function
    def user_address(self, this_state = None, this_bigcity = None, this_city = None, this_zipcode = None, this_address = None):
        if self.address is None:
            self.address = {'state' : this_state, 'bigcity' : this_bigcity, 'city' : this_city, 'zipcode' : this_zipcode, 'address' : this_address}
            self.save()
        else:
            if this_state is not None:
                self.address['state'] = this_state
            if this_bigcity is not None:
                self.address['bigcity'] = this_bigcity
            if this_city is not None:
                self.address['city'] = this_city
            if this_zipcode is not None:
                self.address['zipcode'] = this_zipcode
            if this_address is not None:
                self.address['address'] = this_address
            self.save()

    class Meta:
        ordering = ('id', 'createdate',)   
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

#----------------------------------------------------------------------------------------------------------------------------------------

# Mobile (موبایل) Model
class Mobile (models.Model):
    title = models.CharField(verbose_name='نام', max_length = 225, db_index = True)
    slug = models.SlugField(verbose_name = 'شناسه', unique = True, db_index = True)
    brand = models.CharField(verbose_name = 'برند', max_length = 50)
    description = models.TextField(verbose_name = 'بررسی تخصصی', blank = True, null = True)
    index_image = models.ImageField(verbose_name = 'عکس اصلی', upload_to = 'media/images/mobile/', blank = True, null = True)
    gallery = ArrayField(models.ImageField(verbose_name = 'عکس', upload_to = 'media/images/mobile/'), verbose_name = 'گالری', blank = True, null = True)
    points = JSONField(verbose_name = 'امتیازات', null = True, blank = True)
    price = models.CharField(verbose_name = 'قیمت', max_length = 15)
    discount = models.PositiveSmallIntegerField(verbose_name = 'تخفیف', default = 0)
    FK_Comments = models.ManyToManyField('Comment', verbose_name = 'نظرات', related_name = 'mobile_comments', blank = True)
    colors = ArrayField(models.CharField(verbose_name = 'رنگ', max_length = 9), verbose_name = 'رنگ ها', blank = True, null = True)
    inventory = models.IntegerField(verbose_name = 'موجودی', default = 1)
    guarantees = ArrayField(models.CharField(verbose_name = 'گارانتی', max_length = 225), verbose_name = 'گارانتی ها', blank = True, null = True)
    technical_details = JSONField(verbose_name = 'جزئیات فنی', null = True, blank = True)
    datecreate = models.DateTimeField(verbose_name = 'تاریخ بارگذاری', auto_now_add = True)
    dateupdate = models.DateTimeField(verbose_name = 'تاریخ بروزرسانی', auto_now = True)
    PUBLISH_STATUS =(
        (True,'منتشر شده'),
        (False,'در انتظار تایید'),
    )
    publish = models.BooleanField(verbose_name = 'وضعیت انتشار', choices = PUBLISH_STATUS, default = False)

    def __str__(self):
        return "{}".format(self.title)

    # def get_absolute_url(self):
    #     return reverse("nakhll_market:ProductsDetail", kwargs={
    #         'shop_slug': self.FK_Shop.Slug,
    #         'product_slug': self.Slug,
    #     })

    # def get_add_to_cart_url(self):
    #     return reverse("Payment:add-to-cart", kwargs={
    #         'ID': self.ID
    #     })

    # def get_remove_from_cart_url(self):
    #     return reverse("Payment:remove-from-cart", kwargs={
    #         'ID': self.ID
    #     })

    class Meta:
        ordering = ('id','datecreate',)   
        verbose_name = "موبایل"
        verbose_name_plural = "موبایل ها"

#----------------------------------------------------------------------------------------------------------------------------------------

# Comment (نظر) Model
class Comment(models.Model):
    FK_User = models.ForeignKey(User, verbose_name = 'کاربر', related_name='user_comment', on_delete = models.SET_NULL, null = True)
    title = models.CharField(verbose_name = 'عنوان', max_length = 225)
    description = models.TextField(verbose_name = 'توضیحات')
    likes = JSONField(verbose_name = 'لایک ها', null = True, blank = True)
    replay = JSONField(verbose_name = 'ریپلای ها', null = True, blank = True)
    datecreate = models.DateTimeField(verbose_name = 'تاریخ ثبت', auto_now_add = True)
    STATUS_TYPE = (
        (True,'خوانده شده'),
        (False,'خوانده نشده'),
    )
    status = models.BooleanField(verbose_name = 'وضعیت', choices = STATUS_TYPE, default = False)

    def __str__(self):
        return "{}".format(self.title)

    class Meta:
        ordering = ('id', 'datecreate')   
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"

# --------------------------------------------------------------------------------------------------------------------------------------

# Contact (ارتباط با ما) Model
class Contact(models.Model):
    title = models.CharField(verbose_name = 'عنوان', max_length = 225)
    description = models.TextField(verbose_name = 'توضیحات')
    mobilenumber = models.CharField(verbose_name = 'شماره موبایل', max_length = 11, blank = True)
    email = models.EmailField(verbose_name = 'ایمیل', blank = True)
    createdate = models.DateTimeField(verbose_name = 'تاریخ ایجاد', auto_now_add = True)
    STATUS_TYPE = (
        (0,'بررسی نشده است'),
        (1,'در حال بررسی'),
        (2,'بسته شده است'),
    )
    status = models.PositiveSmallIntegerField(verbose_name = 'وضعیت', choices = STATUS_TYPE, default = 0)

    def __str__(self):
        return "{}".format(self.title)

    class Meta:
        ordering = ('id', 'createdate')
        verbose_name = "ارتباط با ما"
        verbose_name_plural = "ارتباط با ما ها"

# --------------------------------------------------------------------------------------------------------------------------------------