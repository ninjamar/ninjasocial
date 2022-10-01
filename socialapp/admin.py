from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Post, Report, Like, UserFollowing, UserToUserConnection

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Post)
admin.site.register(Report)
admin.site.register(Like)
admin.site.register(UserFollowing)
admin.site.register(UserToUserConnection)