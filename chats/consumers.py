import json
from channels.generic.websocket import AsyncWebsocketConsumer 
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from django.utils import timezone
from chats.models import ChatMessage, ChatRoom


online_users = set()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if not self.user.is_authenticated:
            self.close()
            return
        
        online_users.add(self.user.username)

        self.chatroom_id= self.scope['url_route']['kwargs']['room_id']  
        self.room_group_name = f'chat_{self.chatroom_id}'


        # Join channel layer or channel room
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        
        await self.channel_layer.group_send(self.room_group_name, {
            'type':'online_count',
            'count': len(online_users)
        })

        await self.accept()

    async def disconnect(self, code):
        online_users.remove(self.user.username)
        
        # leave room
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        await self.channel_layer.group_send(self.room_group_name, {
            'type':'online_count',
            'count': len(online_users)
        })

    def save_message(self, message):
        room = ChatRoom.objects.get(room_id=self.chatroom_id)
        ChatMessage.objects.create(sender=self.user, room=room, body=message)

    # Receive message from room group
    async def online_count(self, event):
        count = event['count']
        # Send count to WebSocket
        await self.send(text_data=json.dumps(event))

    async def add_user(self, event):
        await self.send(text_data=json.dumps(event))

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json  = json.loads(text_data)
        message = text_data_json['message']
        time = timezone.now()
        # Send message
        await self.channel_layer.group_send(
            self.room_group_name,                                
            {
                'type': 'chat_message',
                'message':message,
                'user': self.user.username,
                'time': time.isoformat(),
            })
        
        await database_sync_to_async(self.save_message)(message)


    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))