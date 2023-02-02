from django.urls import path
from . import views

app_name = 'Social'

urlpatterns = [
    path('', views.index, name='index'),
    path("profile/<str:username>", views.profile, name="profile"),
    path("posts", views.posts, name="posts"),
    path("about", views.about, name="about"),
    path("settings", views.settings, name="settings"),
    path("search", views.search, name="search"),
    path('staff/reports/', views.reports, name='reports'),
    path("chat/", views.chatindex, name="chat_index"),
    path("chat/group/<int:roomid>/", views.groupchat, name="groupchat"),
    path("chat/uu/<str:u1>/<str:u2>", views.uuchat, name="uuchat"),
    path('logout/', views.logout, name='logout'),
    path("api/create_post", views.create_post, name="create_post"),
    path("api/delete_post/<int:post_id>", views.delete_post, name="delete_post"),
    path("api/report_post/<int:post_id>", views.report_post, name="report_post"),
    path("api/hide_post/<int:post_id>", views.hide_post, name="hide_post"),
    path("api/unhide_post/<int:post_id>", views.unhide_post, name="unhide_post"),
    path("api/ban_user/<int:user_id>", views.ban_user, name="block_user"),
    path("api/unban_user/<int:user_id>", views.unban_user, name="unblock_user"),
    path("api/like_post/<int:post_id>", views.like_post, name="like_post"),
    path("api/unlike_post/<int:post_id>", views.unlike_post, name="unlike_post"),
    path("api/follow_user/<int:user_id>", views.follow_user, name="follow_user"),
    path("api/unfollow_user/<int:user_id>", views.unfollow_user, name="follow_user"),
    path("api/set_about", views.set_about, name="set_about"),
    path("api/nono/delete_account/", views.delete_account, name="delete_account"),
    path("inactive-user/", views.inactive_user, name="inactive_user"),
    path("verification/", views.verification, name="verification")
]
