
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

