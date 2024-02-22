# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import *
from channels.db import database_sync_to_async
import markdown

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'room_{self.room_name}'
        await self.channel_layer.group_add( #type:ignore
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard( #type:ignore
            self.room_group_name,
            self.channel_name
        )
        
    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data['type']
        
        if message_type == 'message':
            message = data.get('message')
            room_id = data.get('room_id')
            user_name = data.get('user_name')
            user_pic = data.get('user_pic')
            sender = data.get('sender')
            
            # Wrap synchronous database access in sync_to_async
            instance_1 = await database_sync_to_async(Friendship.objects.get)(id=room_id)
            instance_2 = await database_sync_to_async(Message.objects.create)(
                content=message,
                sender=sender
            )

            # Update the conversation field in Friendship model
            instance_1.conversation = instance_2
            await database_sync_to_async(instance_1.save)()

            await self.channel_layer.group_send( #type:ignore
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': message,
                'user_name': user_name,
                'user_pic': user_pic,
                'sender': sender
            }
        )
    async def chat_message(self, event):
        message = event['message']
        user_name = event['user_name']
        user_pic = event['user_pic']
        sender = event['sender']
        md = markdown.Markdown(extensions=["fenced_code","codehilite"])
        message = md.convert(message)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message': message, 'user_name': user_name, 'user_pic': user_pic, 'sender': sender}))
