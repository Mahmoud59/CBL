# Generated by Django 3.1.5 on 2021-07-14 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visit', '0005_remove_visit_blocked_students'),
    ]

    operations = [
        migrations.AddField(
            model_name='visit',
            name='email_status',
            field=models.BooleanField(default=False),
        ),
    ]
