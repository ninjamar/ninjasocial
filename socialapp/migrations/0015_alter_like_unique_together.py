# Generated by Django 4.1 on 2022-09-18 00:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialapp', '0014_userfollowing_no_self_rating'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('user', 'post')},
        ),
    ]
