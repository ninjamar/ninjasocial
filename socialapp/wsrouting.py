from django.urls import re_path, path
from .consumers import GroupChatConsumer, UUChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/group/(?P<roomid>\w+)/$', GroupChatConsumer.as_asgi()),
    re_path(r"ws/chat/uu/(?P<u1>[\w.@+-]+)/(?P<u2>[\w.@+-]+)/$", UUChatConsumer.as_asgi())
]
