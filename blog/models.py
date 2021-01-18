from django.contrib.postgres.fields import ArrayField
from django.db.models import JSONField
from django.shortcuts import reverse
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
    # comments = JSONField(verbose_name = 'نظرات', null = True, blank = True)
    comments = ArrayField((models.BigIntegerField(verbose_name= 'نظر')),verbose_name = 'نظرات', blank = True, null = True)
    createdate = models.DateTimeField(verbose_name = 'تاریخ ایجاد', auto_now_add = True)
    updatedate = models.DateTimeField(verbose_name = 'تاریخ بروزرسانی', auto_now = True)
    publishdate = models.DateTimeField(verbose_name = 'تاریخ انتشار', null = True, blank = True)
    PUBLISH_STATUS = (
        (True,'منتشر شده'),
        (False,'منتشر نشده')
    )
    publish = models.BooleanField(verbose_name = 'وضعیت انتشار', choices = PUBLISH_STATUS, default = False)

    def get_url(self):
        return reverse("blog:blog_post", kwargs = {
            'slug': self.slug,
        })

    # points function
    def post_points(self, user_id, this_point):
        if self.points is None:
            data = {}
            data['list'] = []
            this_point = {'user_id': user_id, 'point': this_point}
            data['list'].append(this_point)
            self.points = data
            self.save()
        else:
            status = True
            for item in self.points['list']:
                if item.user_id == user_id:
                    item.point = this_point
                    status = False
            if status:
                this_point = {'user_id': user_id, 'point': this_point}
                self.points['list'].append(this_point)
            self.save()
  
    # get total points
    def get_total_points(self):
        sum_points = 0.0
        for item in self.points['list']:
            sum_points += item.point
        return sum_points

    def get_publishdate_to_jalali(self):
        date_format = "%Y-%m-%d"
        thisdate = datetime.strptime(str(self.publishdate.date()), date_format)
        return str(jdatetime.date.fromgregorian(day = thisdate.day, month = thisdate.month, year = thisdate.year))

    class Meta:
        ordering = ('id', 'createdate', 'publishdate')   
        verbose_name = "پست"
        verbose_name_plural = "پست ها"

# --------------------------------------------------------------------------------------------------------------------------------------