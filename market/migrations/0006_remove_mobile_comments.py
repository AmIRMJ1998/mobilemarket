# Generated by Django 3.1.3 on 2021-01-15 02:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0005_auto_20210114_2316'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mobile',
            name='comments',
        ),
    ]