# Generated by Django 4.1 on 2022-09-19 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialapp', '0017_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.URLField(null=True),
        ),
    ]

