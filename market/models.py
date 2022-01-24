from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.deconstruct import deconstructible
from django.db import models
            
# --------------------------------------------------------------------------------------------------------------------------------------

@deconstructible
class default_json_field():
    def __call__(self):
        return {'list': []}

@deconstructible
class default_address_field():
    def __call__(self):
        return {'mobile': None, 'state': None, 'city': None, 'zipcode': None, 'address': None}

# --------------------------------------------------------------------------------------------------------------------------------------

class UserManager(BaseUserManager):
    def create_user(self,username,email=None,first_name=None,last_name=None,password=None,**kwargs):
        if not username:
            raise ValueError("Users must have username")
        if not password:
            raise ValueError("Users must have password")
        if not email:
            raise ValueError("Users must have email")
        if not first_name:
            raise ValueError("Users must have first_name")
        if not last_name:
            raise ValueError("Users must have last_name")
        user = self.model(username=username,email=email,first_name=first_name,last_name=last_name,**kwargs)
        user.set_password(password)
        user.save()
        return user
    
    def create_staffuser(self,username,email=None,first_name=None,last_name=None,password=None,**kwargs):
        user = self.model(username=username,email=email,first_name=first_name,last_name=last_name,staff=True,**kwargs)
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self,username,email=None,first_name=None,last_name=None,password=None,**kwargs):
        user = self.model(username=username,email=email,first_name=first_name,last_name=last_name,staff=True,superuser=True,**kwargs)
        user.set_password(password)
        user.save()
        return user
        
# --------------------------------------------------------------------------------------------------------------------------------------

# User (کاربر) Model
class User (AbstractBaseUser):
    username = models.CharField(verbose_name='username',max_length=50,unique=True,db_index=True)
    first_name = models.CharField(verbose_name='first name',max_length=150)
    last_name = models.CharField(verbose_name='last name',max_length=300)
    email = models.EmailField(verbose_name='email',unique=True)
    mobile = models.CharField(verbose_name='شماره موبایل',max_length=11,null=True)
    state = models.CharField(verbose_name='استان',max_length=50,null=True)
    city = models.CharField(verbose_name='شهر',max_length=50,null=True)
    zipcode = models.CharField(verbose_name='کدپستی',max_length=10,null=True)
    address = models.TextField(verbose_name='آدرس',null=True)
    active = models.BooleanField(verbose_name='وضعیت فعالیت',default=True)
    superuser = models.BooleanField(verbose_name='وضعیت مدیریت',default=False)
    staff = models.BooleanField(verbose_name= 'وضعیت کارمندی',default=False)
    favorite_list = models.JSONField(verbose_name='لیست علاقه مندی ها',default=default_json_field())
    create_date = models.DateTimeField(verbose_name='تاریخ عضویت',auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='تاریخ عضویت',auto_now_add=True)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email','first_name','last_name']

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

    def get_fullname(self):
        return '{} {}'.format(self.first_name, self.last_name)

    class Meta:
        ordering = ('id','create_date')   
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

#----------------------------------------------------------------------------------------------------------------------------------------

# Mobile (موبایل) Model
class Mobile (models.Model):
    title = models.CharField(verbose_name='عنوان',max_length=255,unique=True,db_index=True)
    slug = models.SlugField(verbose_name='شناسه',max_length= 50,unique=True,db_index=True)
    brand = models.CharField(verbose_name = 'برند', max_length = 50)
    description = RichTextUploadingField(verbose_name='بررسی تخصصی',null=True)
    index_image = models.ImageField(verbose_name='عکس اصلی',upload_to='media/images/mobile/')
    gallery = models.JSONField(verbose_name='گالری',default=default_json_field())
    price = models.PositiveIntegerField(verbose_name='قیمت')
    discount = models.PositiveIntegerField(verbose_name='تخفیف',default=0)
    technical_details = models.JSONField(verbose_name='جزئیات فنی',default=default_json_field())
    guarantees = models.JSONField(verbose_name='گارانتی',default=default_json_field())
    points = models.JSONField(verbose_name='امتیازات',default=default_json_field())
    colors = models.JSONField(verbose_name='رنگ ها',default=default_json_field())
    publish = models.BooleanField(verbose_name='وضعیت انتشار',default=True)
    create_date = models.DateTimeField(verbose_name='تاریخ بارگذاری',auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='تاریخ بروزرسانی',auto_now=True)

    def __str__(self):
        return "{} ({})".format(self.title,self.slug)

    def get_points_count(self):
        userCount = len(self.points['list'])
        point = 0
        for item in self.points['list']:
            point += item['rate']
        averagePoint = round(float(point / userCount))
        return averagePoint

    def set_point(self,userID,rate):
        objectExists = False
        for item in self.points['list']:
            if item['user'] == userID:
                self.points['list'].remove(item)
                objectExists = True
                break
        if not objectExists:
            self.points['list'].append({'user': userID, 'rate': rate})
        self.save()

    class Meta:
        ordering = ('id','create_date')   
        verbose_name = 'موبایل'
        verbose_name_plural = 'موبایل ها'

#----------------------------------------------------------------------------------------------------------------------------------------

# Comment (نظر) Model
class Comment(models.Model):
    fk_user = models.ForeignKey(User,verbose_name='کاربر',related_name='user_comment',on_delete=models.SET_NULL,null=True)
    fk_mobile = models.ForeignKey(Mobile,verbose_name='موبایل',related_name='mobile_comment',on_delete=models.SET_NULL,null=True)
    text = models.TextField(verbose_name = 'متن')
    likes = models.JSONField(verbose_name='لایک',default=default_json_field())
    fk_parent = models.ForeignKey('self',verbose_name='کامنت پدر',related_name='comment_replay',on_delete=models.SET_NULL,null=True)
    create_date = models.DateTimeField(verbose_name='تاریخ ثبت',auto_now_add=True)

    def __str__(self):
        return "{} - {}".format(self.fk_user,self.fk_mobile)

    def set_like(self,userID):
        if userID in self.likes['list']:
            self.likes['list'].remove(item)
        else:
            self.likes['list'].append(userID)
        self.save()

    class Meta:
        ordering = ('id','create_date')   
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'

# --------------------------------------------------------------------------------------------------------------------------------------

# Contact (ارتباط با ما) Model
class Contact(models.Model):
    title = models.CharField(verbose_name='عنوان',max_length=255)
    text = models.TextField(verbose_name='متن')
    mobile = models.CharField(verbose_name='شماره موبایل',max_length=11,null=True)
    email = models.EmailField(verbose_name='ایمیل',null=True)
    create_date = models.DateTimeField(verbose_name='تاریخ ساخت',auto_now_add=True)
    STATUS_TYPE = (
        (0,'بررسی نشده است'),
        (1,'در حال بررسی'),
        (2,'بسته شده است'),
    )
    status = models.PositiveSmallIntegerField(verbose_name='وضعیت',choices=STATUS_TYPE,default=0)

    def __str__(self):
        return "{}".format(self.title)

    class Meta:
        ordering = ('id','create_date')
        verbose_name = 'ارتباط با ما'
        verbose_name_plural = 'ارتباط با ما ها'

# --------------------------------------------------------------------------------------------------------------------------------------

# Slider (اسلایدر) Model
class Slider(models.Model):
    image = models.ImageField(verbose_name='عکس',upload_to='media/images/slider/')
    description = models.CharField(verbose_name='برچسب روی اسلایدر',max_length=50,null=True)
    link = models.URLField(verbose_name='لینک',null=True)
    publish = models.BooleanField(verbose_name='وضعیت انتشار',default=True)

    class Meta:
        ordering = ('id',)   
        verbose_name = 'اسلایدر'
        verbose_name_plural = 'اسلایدر ها'
    
#----------------------------------------------------------------------------------------------------------------------------------

# Message (پیام) Model
class Message(models.Model):
    title = models.CharField(verbose_name='عنوان',max_length=50)
    text = models.TextField(verbose_name='متن')
    users = models.JSONField(verbose_name='کاربران',default=default_json_field())
    create_date = models.DateTimeField(verbose_name='تاریخ ساخت',auto_now_add=True)

    def __str__(self):
        return "{} ({})".format(self.title, self.create_date)

    class Meta:
        ordering = ('id','create_date')
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام ها'

#----------------------------------------------------------------------------------------------------------------------------------

# Factor (فاکتور) Model 
class Factor(models.Model):
    code = models.CharField(verbose_name='کد',max_length=10,unique=True,db_index=True)
    fk_user = models.ForeignKey(User,verbose_name='کاربر',related_name='user_factor',on_delete=models.SET_NULL,null=True)
    address = models.JSONField(verbose_name='آدرس',default=default_address_field())
    items = models.JSONField(verbose_name='محصولات',default=default_json_field())
    post_price = models.PositiveIntegerField(verbose_name='هزینه پست',default=0) 
    total_price = models.PositiveIntegerField(verbose_name='هزینه کل',default=0)
    PAYMENT_STATUS = (
        (True,'پرداخت شد'),
        (False,'پرداخت نشده')
    )
    payment_status = models.BooleanField(verbose_name='وضعیت پرداخت',choices=PAYMENT_STATUS,default=False)
    FACTOR_STATUS = (
        (0,'فاکتور پرداخت نشده است'),
        (1,'فاکتور در حال آماده سازی'),
        (2,'سفارش آماده است'),
        (3,'سفارش ارسال شده است'),
        (4,'فاکتور لغو شده است'),
    )
    status = models.PositiveSmallIntegerField(verbose_name='وضعیت فاکتور',choices=FACTOR_STATUS,default=0)
    order_date = models.DateTimeField(verbose_name='تاریخ و زمان سفارش',auto_now_add=True)

    def __str__(self):
        return "{} ({})".format(self.fk_user,self.code)

    def save(self, *args, **kwargs):
        if len(self.code) == 0:
            if Factor.objects.exists():
                count = Factor.objects.count()
                while 1:
                    newCode = 'F-' + str(count + 1).zfill(8)
                    if not Factor.objects.filter(code=newCode).exists():
                        self.code = newCode
                        break
            else:
                newCode = 'F-' + str(1).zfill(8)
                self.code = newCode
        super(Factor, self).save(*args, **kwargs)

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
        thisdate = datetime.strptime(str(self.order_date.date()), date_format)
        return str(jdatetime.date.fromgregorian(day = thisdate.day, month = thisdate.month, year = thisdate.year))

    class Meta:
        ordering = ('id','order_date')
        verbose_name = 'فاکتور'
        verbose_name_plural = 'فاکتور ها'

#----------------------------------------------------------------------------------------------------------------------------------
