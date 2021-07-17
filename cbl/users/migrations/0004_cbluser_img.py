# Generated by Django 3.1.5 on 2021-03-28 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("users", "0003_cbluser_department")]

    operations = [
        migrations.AddField(
            model_name="cbluser",
            name="img",
            field=models.ImageField(
                default="", upload_to="storage/users/", verbose_name="user picture"
            ),
            preserve_default=False,
        )
    ]
