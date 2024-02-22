from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from .models import *
from django.utils import timezone

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Assign user to a specific room (e.g., based on authentication)
        self.room_name = self.scope['url_route']['kwargs']['room_id'] 
        self.user_id = self.scope['user'].id
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
    
        await self.channel_layer.group_send(#type:ignore
            self.room_name,
            {
                'type': 'game_message',
                'message': f'Player {self.user_id} has left.'
            }
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
""" 
class ChessConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.game_id = self.scope['url_route']['kwargs']['room_id']
        self.user_id = self.scope['user'].id

        # Generate the game group name based on the game_id
        self.game_group_name = f'game_{self.game_id}'

        # Join the game group
        await self.channel_layer.group_add(
            self.game_group_name,
            self.channel_name
        )
        
        await self.accept()

        # Notify the group when someone joins
        await self.channel_layer.group_send(
            self.game_group_name,
            {
                'type': 'game_message',
                'message': f'A Player has joined.',
            }
        )
        
    async def disconnect(self, close_code):
        # Leave the game group
        await self.channel_layer.group_discard(
            self.game_group_name,
            self.channel_name
        )

        # Notify the group when someone leaves
        await self.channel_layer.group_send(
            self.game_group_name,
            {
                'type': 'game_message',
                'message': f'Player {self.user_id} has left.'
            }
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        move_type = data['type']

        # Handle different types of messages
        if move_type == 'on_Drag':
            await self.channel_layer.group_send(
                self.game_group_name,
                {
                    'type': 'game_message',
                    'message': f'Player {self.user_id} is dragging a piece.'
                }
            )
        elif move_type == 'on_Drop':
            source, target = data['sum'][:2], data['sum'][2:]
            self.move_message = f'{source}-{target}'
            
            # Send move to game group
            await self.channel_layer.group_send(
                self.game_group_name,
                {
                    'type': 'game_move',
                    'move_message': f'Player {self.user_id} moved {self.move_message}',
                    'movement': source + target,
                }
            )
        
        elif move_type == 'result':
            result = data.get('msg')
            instance = await database_sync_to_async(Game.objects.get)(id=self.game_id)
            instance.result = result
            await database_sync_to_async(instance.save)()
            

    async def game_move(self, event):
        move_message = event['move_message']
        movement = event['movement']

        # Send move message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'game_move',
            'move_message': move_message,
            'movement': movement,
        }))

    async def game_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'game_message',
            'message': message,
        })) """