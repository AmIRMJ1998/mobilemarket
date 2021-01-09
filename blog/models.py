from django.contrib.postgres.fields import ArrayField
from django.db.models import JSONField
from datetime import datetime
from django.db import models
import os, jdatetime

# --------------------------------------------------------------------------------------------------------------------------------------

# Post (پست) Model
class Post (models.Model):
    title = models.CharField(verbose_name = 'عنوان', max_length = 255)
    slug = models.SlugField(verbose_name = 'شناسه', unique = True)
    text = models.TextField(verbose_name = 'متن')
    index_image = models.ImageField(verbose_name = 'عکس اصلی', upload_to = 'media/images/blog/', null = True, blank = True)
    slider_image = models.ImageField(verbose_name = 'عکس اسلایدر', upload_to = 'media/images/blog/', null = True, blank = True)
    points = JSONField(verbose_name = 'امتیازات', null = True, blank = True)
    comments = JSONField(verbose_name = 'نظرات', null = True, blank = True)
    createdate = models.DateTimeField(verbose_name = 'تاریخ ایجاد', auto_now_add = True)
    updatedate = models.DateTimeField(verbose_name = 'تاریخ بروزرسانی', auto_now = True)
    publishdate = models.DateTimeField(verbose_name = 'تاریخ انتشار', null = True, blank = True)
    PUBLISH_STATUS = (
        (True,'منتشر شده'),
        (False,'منتشر نشده')
    )
    publish = models.BooleanField(verbose_name = 'وضعیت انتشار', choices = PUBLISH_STATUS, default = False)

    def get_index_image_url(self):
        return self.index_image.url

    def get_slider_image_url(self):
        return self.slider_image.url

    def get_publishdate_to_jalali(self):
        date_format = "%Y-%m-%d"
        thisdate = datetime.strptime(str(self.publishdate.date()), date_format)
        return str(jdatetime.date.fromgregorian(day = thisdate.day, month = thisdate.month, year = thisdate.year))

    class Meta:
        ordering = ('id', 'createdate', 'publishdate')   
        verbose_name = "پست"
        verbose_name_plural = "پست ها"

# --------------------------------------------------------------------------------------------------------------------------------------