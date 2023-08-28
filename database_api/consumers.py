# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class NotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         await self.channel_layer.group_add("notifications", self.channel_name)

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard("notifications", self.channel_name)

#     async def send_notification(self, event):
#         user = self.scope["user"]
#         if user.is_authenticated and not user.is_staff:
#             user_uuid = user.uuid  # Replace with the actual attribute name for the user UUID
#             notification = event['message']
#             if notification['uuid'] == user_uuid:
#                 await self.send(text_data=json.dumps(notification))


import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token
from asgiref.sync import sync_to_async

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope['user'].is_authenticated:
            print(self.scope['user'].uuid)
            await self.accept()
            await self.channel_layer.group_add(self.scope['user'].uuid, self.channel_name)
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.scope['user'].uuid, self.channel_name)

    async def send_notification(self, event):
        notification = event['message']
        await self.send(text_data=json.dumps(notification))



# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from django.contrib.auth.models import AnonymousUser
# from django.contrib.auth import get_user_model
# from django.db import close_old_connections
# from rest_framework.authtoken.models import Token

# User = get_user_model()

# class NotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # Establish the WebSocket connection
#         await self.accept()

#         # Authenticate the user and add user information to the scope
#         await self.authenticate_user()

#         # Add the consumer to the "notifications" group
#         await self.channel_layer.group_add("notifications", self.channel_name)

#     async def disconnect(self, close_code):
#         # Remove the consumer from the "notifications" group
#         await self.channel_layer.group_discard("notifications", self.channel_name)

#     async def send_notification(self, event):
#         # Send a notification to the connected user (if authenticated)
#         if hasattr(self.scope, "user") and self.scope["user"].is_authenticated and not self.scope["user"].is_staff:
#             user_uuid = self.scope["user"].uuid  # Replace with the actual attribute name for the user UUID
#             notification = event['message']
#             if notification['uuid'] == user_uuid:
#                 await self.send(text_data=json.dumps(notification))

#     @database_sync_to_async
#     def authenticate_user(self):
#         close_old_connections()
#         self.scope["user"] = AnonymousUser()
#         if self.scope.get("session"):
#             if "token" in self.scope["session"]:
#                 token_key = self.scope["session"]["token"]
#                 user = Token.objects.get(key=token_key).user
#                 if user and user.is_authenticated and not user.is_staff:
#                     self.scope["user"] = user
