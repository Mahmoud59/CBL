# Generated by Django 3.1.5 on 2021-04-06 15:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('visit', '0003_auto_20210328_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='visit',
            name='blocked_students',
            field=models.ManyToManyField(limit_choices_to={'is_staff': False, 'is_super_admin': False, 'is_superuser': False}, related_name='blocked_students', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='visit',
            name='img_one',
            field=models.ImageField(blank=True, upload_to='storage/visits/', verbose_name='Other image'),
        ),
        migrations.AlterField(
            model_name='visit',
            name='img_two',
            field=models.ImageField(blank=True, upload_to='storage/visits/', verbose_name='Other image'),
        ),
        migrations.AlterField(
            model_name='visit',
            name='main_img',
            field=models.ImageField(blank=True, upload_to='storage/visits/', verbose_name='Main image'),
        ),
    ]
