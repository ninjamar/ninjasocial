# Generated by Django 4.1 on 2022-09-18 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialapp', '0013_alter_userfollowing_to_follow_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='userfollowing',
            constraint=models.CheckConstraint(check=models.Q(('who_follows', models.F('to_follow')), _negated=True), name='no_self_rating'),
        ),
    ]
