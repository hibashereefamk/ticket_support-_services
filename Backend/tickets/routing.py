from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Note the trailing slash: /
    re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
]