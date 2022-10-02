# Generated by Django 4.1 on 2022-09-16 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialapp', '0007_post_is_custom_post_is_dev_post_is_tester'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='is_custom',
        ),
        migrations.RemoveField(
            model_name='post',
            name='is_dev',
        ),
        migrations.RemoveField(
            model_name='post',
            name='is_tester',
        ),
        migrations.AddField(
            model_name='user',
            name='is_custom',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_dev',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_tester',
            field=models.BooleanField(default=False),
        ),
    ]