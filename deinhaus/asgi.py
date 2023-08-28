
# ASGI config for deinhaus project.

# It exposes the ASGI callable as a module-level variable named ``application``.


import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from database_api import routing
from database_api import consumers
from django.urls import re_path
from channels.auth import AuthMiddlewareStack
from database_api.token_auth import TokenAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deinhaus.settings')


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": TokenAuthMiddleware(
        URLRouter([
            re_path(r'ws/notifications/$',
                    consumers.NotificationConsumer.as_asgi()),
        ]),
    ),
})
