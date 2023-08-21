import json
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Room, Message
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        room_id = self.scope['url_route']['kwargs']['pk']
        self.room_id = room_id
        print(room_id)

        self.room_group_name = f'chat_{room_id}'
        print("adding ig")
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = text_data_json['user']

        if str(user) == str(self.scope.get('user')) and len(message) > 0 and message.strip() != '':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'msg_data': {'user': user, 'message': message},
                }
            )

    async def chat_message(self, event):
        message_data = event['msg_data']
        message = message_data.get('message')
        user = message_data.get('user')

        # Check if the user matches self.scope.get('user')

        print("here")
        room = await sync_to_async(Room.objects.get)(id=self.room_id)
        user1 = await sync_to_async(User.objects.get)(username=user)
        await sync_to_async(Message.objects.create)(
            room=room,
            user=user1,
            body=message
        )

        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
            'type': 'message',
        }))
