# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from .models import *

""" class OnlineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        # Handle user connection, mark user as online, etc.
        self.user = self.scope['user']

        if isinstance(self.user, CustomUser):  # Ensure it's an instance of your CustomUser model
            self.user.mark_online()

            # Notify other clients about the user's online status
            await self.send_status_update('online')

    async def disconnect(self, close_code):
        # Handle user disconnection, mark user as offline, etc.
        if isinstance(self.user, CustomUser):  # Ensure it's an instance of your CustomUser model
            self.user.mark_offline()

            # Notify other clients about the user's offline status
            await self.send_status_update('offline')

    async def send_status_update(self, status):
        await self.send(text_data=json.dumps({
            'status': status,
            'username': self.user.username,
        })) """

class YourConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        channel_layer = get_channel_layer()
        await channel_layer.group_add( #type:ignore
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        channel_layer = get_channel_layer()
        await channel_layer.group_discard(#type:ignore
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        # Send message to room group
        channel_layer = get_channel_layer()
        await channel_layer.group_send(#type:ignore
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message': message}))