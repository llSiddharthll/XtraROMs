from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from .models import *
from django.utils import timezone

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Assign user to a specific room (e.g., based on authentication)
        self.room_name = self.scope['url_route']['kwargs']['room_id'] 
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(#type:ignore
            self.room_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(#type:ignore
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json['message']
        pfp = text_data_json['pfp']

        # Get the receiver (assuming it's available in your scope)
        receiver = self.scope['user']

        # Store message in the database
        await self.save_message(message_content, self.scope['user'], receiver)

        # Send message to all clients in the room
        await self.channel_layer.group_send(#type:ignore
            self.room_name,
            {
                'type': 'chat_message',
                'message': message_content,
                'sender': self.scope['user'].username,
                'receiver': receiver.username,
                'pfp': pfp,
            }
        )

    
    @database_sync_to_async
    def save_message(self, message_content, sender, receiver):
        return Message.objects.create(
            content=message_content,
            sender=sender,
            receiver=receiver,
            timestamp=timezone.now() 
        )


    async def chat_message(self, event):
        message = event.get('message', '')
        username = event.get('sender', '')
        profile_picture_url = event.get('pfp', '')
        # Send the message to the connected WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'pfp': profile_picture_url,
        }))