from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from database_api import consumers
from django.urls import re_path


websocket_urlpatterns = [
    re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
  
]
