from ckeditor_uploader.fields import RichTextUploadingField
from market.models import default_json_field
from market.models import User
from django.db import models

# --------------------------------------------------------------------------------------------------------------------------------------

# Post (پست) Model
class Post (models.Model):
    title = models.CharField(verbose_name='عنوان',max_length=255)
    slug = models.SlugField(verbose_name='شناسه',unique=True)
    description = RichTextUploadingField(verbose_name='متن')
    index_image = models.ImageField(verbose_name='عکس اصلی',upload_to='media/images/blog/')
    slider_image = models.ImageField(verbose_name='عکس اسلایدر',upload_to='media/images/blog/')
    points = models.JSONField(verbose_name='امتیازات',default=default_json_field())
    publish = models.BooleanField(verbose_name='وضعیت انتشار',default=True)
    create_date = models.DateTimeField(verbose_name='تاریخ ایجاد',auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='تاریخ بروزرسانی',auto_now=True)

    class Meta:
        ordering = ('id','create_date',)   
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'

# --------------------------------------------------------------------------------------------------------------------------------------

# PostComment (نظرات بلاگ) Model
class PostComment(models.Model):
    fk_user = models.ForeignKey(User,verbose_name='کاربر',related_name='user_post_comment',on_delete=models.SET_NULL,null=True)
    fk_post = models.ForeignKey(Post,verbose_name='پست',related_name='post_comment',on_delete=models.SET_NULL,null=True)
    text = models.TextField(verbose_name = 'متن')
    likes = models.JSONField(verbose_name='لایک',default=default_json_field())
    fk_parent = models.ForeignKey('self',verbose_name='کامنت پدر',related_name='post_comment_replay',on_delete=models.SET_NULL,null=True)
    create_date = models.DateTimeField(verbose_name='تاریخ ثبت',auto_now_add=True)

    def __str__(self):
        return "{} - {}".format(self.fk_user,self.fk_post)

    def set_like(self,userID):
        if userID in self.likes['list']:
            self.likes['list'].remove(item)
        else:
            self.likes['list'].append(userID)
        self.save()

    class Meta:
        ordering = ('id','create_date')   
        verbose_name = 'نظر پست'
        verbose_name_plural = 'نظرات پست'

# --------------------------------------------------------------------------------------------------------------------------------------
