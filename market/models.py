from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.postgres.fields import ArrayField
from django.utils.deconstruct import deconstructible
from django.db.models import JSONField
from django_jalali.db import models as jmodels
from datetime import datetime
from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
import os, jdatetime

# factor number function
@deconstructible
class factor_number():
    def __init__(self, this_size):
        self.size = this_size

    def __call__(self):
        if Factor.objects.filter(number = self.extend('1')).exists():
            last = Factor.objects.latest('orderdate').number
            i = 1
            while 1:
                value = self.extend(str(int(last) + i))
                if not Factor.objects.filter(number = value).exists():
                    return value
                else:
                    i += 1
        else:
            return self.extend('1')

    def extend(self, value):
        count = self.size - len(value)
        if count == 0:
            return value
        else:
            result = ''
            while count > 0:
                result += '0'
                count -= 1
            result += value
            return result
            
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
    address = JSONField(verbose_name = 'آدرس', blank = True, null = True)
    active = models.BooleanField(verbose_name = 'وضعیت فعالیت', default = True)
    superuser = models.BooleanField(verbose_name = 'وضعیت مدیریت', default = False)
    staff = models.BooleanField(verbose_name = 'وضعیت کارمندی', default = False)
    citypercode = models.CharField(verbose_name = 'پیش شماره', max_length = 3, blank = True, null = True)
    phone = models.CharField(verbose_name = 'شماره تلفن ثابت', max_length = 8, blank = True)
    birthday = jmodels.jDateField(verbose_name = 'تاریخ تولد', null = True)
    comment_list = JSONField(verbose_name = 'لیست نظرات ها', null = True, blank = True)
    factor_list = JSONField(verbose_name = 'لیست فاکتور ها', null = True, blank = True)
    message_list = JSONField(verbose_name = 'لیست پیام ها', null = True, blank = True)
    favorite_list = ArrayField(models.BigIntegerField(verbose_name = 'محصول مورد علاقه'), verbose_name = 'لیست محصولات مورد علاقه', null = True, blank = True)
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
    def user_address(self, this_state = None, this_city = None, this_zipcode = None, this_address = None):
        if self.address is None:
            self.address = {'state' : this_state, 'city' : this_city, 'zipcode' : this_zipcode, 'address' : this_address}
            self.save()
        else:
            if this_state is not None:
                self.address['state'] = this_state
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
    slug = models.SlugField(verbose_name = 'شناسه', unique = True, db_index = True, max_length= 100)
    brand = models.CharField(verbose_name = 'برند', max_length = 50)
    # description = models.TextField(verbose_name = 'بررسی تخصصی', blank = True, null = True)
    description = RichTextUploadingField(verbose_name = 'بررسی تخصصی', blank = True, null = True)
    index_image = models.ImageField(verbose_name = 'عکس اصلی', upload_to = 'media/images/mobile/', blank = True, null = True)
    # gallery = ArrayField(models.ImageField(verbose_name = 'عکس', upload_to = 'media/images/mobile/'), verbose_name = 'گالری', blank = True, null = True)
    points = JSONField(verbose_name = 'امتیازات', null = True, blank = True)
    price = models.CharField(verbose_name = 'قیمت', max_length = 15)
    discount = models.CharField(verbose_name = 'تخفیف', max_length = 15, default='0')
    comments = ArrayField((models.BigIntegerField(verbose_name= 'نظر')),verbose_name = 'نظرات', blank = True, null = True)
    colors = JSONField(verbose_name = 'رنگ ها', blank = True, null = True)
    inventory = models.IntegerField(verbose_name = 'موجودی', default = 1)
    guarantees = ArrayField(models.CharField(verbose_name = 'گارانتی', max_length = 225), verbose_name = 'گارانتی ها', blank = True, null = True)
    technical_details = JSONField(verbose_name = 'جزئیات فنی', blank = True, null = True)
    datecreate = models.DateTimeField(verbose_name = 'تاریخ بارگذاری', auto_now_add = True)
    dateupdate = models.DateTimeField(verbose_name = 'تاریخ بروزرسانی', auto_now = True)
    PUBLISH_STATUS =(
        (True,'منتشر شده'),
        (False,'در انتظار تایید'),
    )
    publish = models.BooleanField(verbose_name = 'وضعیت انتشار', choices = PUBLISH_STATUS, default = False)

    def __str__(self):
        return "{}".format(self.title)

    def total_point(self):
        totalPoint = 0
        pointCount = 0
        for item in self.points:
            totalPoint += float(item['productRate'])
            pointCount += 1
        averagePoint = float(totalPoint / pointCount)
        return averagePoint
    
    def real_price(self):
        discountInt = int(self.discount)
        priceInt = int(self.price)
        return discountInt + priceInt


    def product_rate_set(self, userID = None, productRate = None):
        if self.points is None:
            self.points = [{'userID' : userID, 'productRate' : productRate},]
            self.save()
        else:
            if self.points is not None:
                for item in self.points:
                    if item['userID'] == userID:
                        item['productRate'] = productRate
                        self.save()
                    else:
                        self.points.append({'userID': userID, 'productRate': productRate},)
                        self.save()

    # @property
    def inventory_by_color(self):
        inventory = 0
        for color in self.colors:
            for _, value in color.items():
                for __, invent in value.items():
                    inventory += invent


    def get_total_price(self, this_count):
        return int(self.price) * int(this_count)

    #     return inventory

    # def save(self, *args, **kwargs):
    #     inventory = 0
    #     for color in self.colors:
    #         for _, value in color.items():
    #             for __, invent in value.items():
    #                 inventory += invent
    #     self.inventory = inventory
    #     super(Mobile, self).save(*args, **kwargs)

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
    FK_User = models.ForeignKey(User, verbose_name = 'کاربر', related_name = 'user_comment', on_delete = models.SET_NULL, null = True)
    description = models.TextField(verbose_name = 'توضیحات')
    likes = ArrayField(models.BigIntegerField(verbose_name ='لایک'), verbose_name = 'لایک ها', null = True, blank = True)
    replay = ArrayField(models.BigIntegerField(verbose_name ='لایک'), verbose_name = 'ریپلای ها', null = True, blank = True)
    datecreate = jmodels.jDateTimeField(verbose_name = 'تاریخ ثبت', auto_now_add = True)

    def __str__(self):
        return "{} : {}".format(self.FK_User, self.datecreate)

    class Meta:
        ordering = ('id', 'datecreate')   
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"

    def like_count(self):
        pointCount = 0
        for _ in self.likes:
            pointCount += 1
        return pointCount

    def summary(self):
        return str(self.description)[:50] + '...'


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

# Slider (اسلایدر) Model
class Slider(models.Model):
    image = models.ImageField(verbose_name='عکس', upload_to = 'media/images/slider/')
    description = models.CharField(verbose_name = 'برچسب روی اسلایدر', max_length = 150, blank = True, null = True)
    link = models.URLField(verbose_name = 'لینک', blank = True, null = True)
    PUBLISH_STATUS = (
        (True,'منتشر شده'),
        (False,'منتشر نشده'),
    )
    publish = models.BooleanField(verbose_name = 'وضعیت انتشار', choices = PUBLISH_STATUS, default = True)

    def __str__(self):
        return "{}".format(self.description)

    class Meta:
        ordering = ('id', )   
        verbose_name = "اسلایدر"
        verbose_name_plural = "اسلایدر ها"
    
#----------------------------------------------------------------------------------------------------------------------------------

# Message (پیام) Model
class Message(models.Model):
    title = models.CharField(verbose_name = 'عنوان', db_index = True, max_length = 225)
    text = models.TextField(verbose_name = 'متن')
    SEEN_STATUS = (
        (True,'دیده شده'),
        (False,'دیده نشده'),
    )
    users = JSONField(verbose_name = 'کاربران', blank = True, null = True)
    datetime = jmodels.jDateTimeField(verbose_name = 'تاریخ و زمان ثبت', auto_now_add = True)

    def __str__(self):
        return "{} ({})".format(self.title, self.datetime)

    def summary(self):
        return str(self.text)[:50] + '...'

    class Meta:
        ordering = ('id',)
        verbose_name = "پیام"
        verbose_name_plural = "پیام ها"


#----------------------------------------------------------------------------------------------------------------------------------

# Factor (فاکتور) Model 
class Factor(models.Model):
    number = models.CharField(verbose_name = 'شماره فاکتور', max_length = 5, unique = True, default = factor_number(5))
    FK_User = models.ForeignKey(User, verbose_name = 'کاربر', on_delete = models.SET_NULL, related_name = 'user_factor', null = True)
    address = JSONField(verbose_name = 'آدرس', blank = True, null = True)
    items = JSONField(verbose_name = 'محصولات', blank = True, null = True)
    post_price = models.CharField(verbose_name = 'هزینه پست', max_length = 15, default = '0') 
    total_price = models.CharField(verbose_name = 'هزینه کل', max_length = 15, default = '0')
    PAYMENT_STATUS = (
        (True,'پرداخت شد'),
        (False,'پرداخت نشده'),
    )
    payment_status = models.BooleanField(verbose_name = 'وضعیت پرداخت', choices = PAYMENT_STATUS, default = False)
    orderdate = models.DateTimeField(verbose_name = 'تاریخ و زمان ثبت', auto_now_add = True)
    FACTOR_STATUS = (
        (0,'فاکتور پرداخت نشده است'),
        (1,'فاکتور در حال آماده سازی'),
        (2,'سفارش آماده است'),
        (3,'سفارش ارسال شده است'),
        (4,'فاکتور لغو شده است'),
    )
    status = models.PositiveSmallIntegerField(verbose_name = 'وضعیت فاکتور', choices = FACTOR_STATUS, default = 0)

    def __str__(self):
        return "{} ({})".format(self.number, self.FK_User)

    # add item in factor function
    def add_item(self, this_mobile, this_count, this_color, this_color_value, this_guarantee):
        if self.items is None:
            data = {}
            data['items'] = []
            this_item = {'id': this_mobile.id, 'title': this_mobile.title, 'price': this_mobile.price, 'total_price': this_mobile.get_total_price(this_count), 'count': this_count, 'color': this_color, 'color_value': this_color_value, 'guarantee': this_guarantee}
            data['items'].append(this_item) 
            self.items = data
            self.save()
        else:
            status = True
            for item in self.items['items']:
                if (item['id'] == this_mobile.id) and (item['color'] == this_color) and (item['guarantee'] == this_guarantee):
                    if int(item['count']) + 1 > this_mobile.inventory:
                        status = False
                    else:
                        item['count'] += this_count
                        item['total_price'] = this_mobile.get_total_price(item['count'])
                        status = False
            if status:
                this_item = {'id': this_mobile.id, 'title': this_mobile.title, 'price': this_mobile.price, 'total_price': this_mobile.get_total_price(this_count), 'count': this_count, 'color': this_color, 'color_value': this_color_value, 'guarantee': this_guarantee}
                self.items['items'].append(this_item) 
                # self.items = data
            self.save()

   # address function
    def add_address(self, this_state, this_city, this_zipcode, this_address, this_phone, this_per_city_code, this_mobile):
        self.address = {'state' : this_state, 'city' : this_city, 'zipcode' : this_zipcode, 'address' : this_address, 'phone' : this_phone, 'per_city_code' : this_per_city_code, 'mobile': this_mobile}
        self.save()

    def get_total_price(self):
        total_sum = 0
        for item in self.items['items']:
            total_sum += item['total_price']
        return total_sum

    def get_orderdate_to_jalali(self):
        date_format = "%Y-%m-%d"
        thisdate = datetime.strptime(str(self.orderdate.date()), date_format)
        return str(jdatetime.date.fromgregorian(day = thisdate.day, month = thisdate.month, year = thisdate.year))

    class Meta:
        ordering = ('id', 'orderdate')
        verbose_name = "فاکتور"
        verbose_name_plural = "فاکتور ها"

#----------------------------------------------------------------------------------------------------------------------------------
