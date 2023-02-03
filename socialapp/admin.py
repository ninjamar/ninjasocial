from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Post, Report, Like, UserFollowing, UserToUserConnection


# we need to automate auth0 account deletion
# make user verified action
# automate actions
# automate tokenization and renewal
class MyUserAdmin(UserAdmin):
    actions = ['mydelete_model']

    def get_actions(self, request):
        self._actions = super(UserAdmin, self).get_actions(request)
        return self._actions

    def mydelete_model(self, request, obj):
        self._actions["delete_selected"][0](self, request, self.get_queryset(request))
    mydelete_model.short_description = 'Delete user test'


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Post)
admin.site.register(Report)
admin.site.register(Like)
admin.site.register(UserFollowing)
admin.site.register(UserToUserConnection)