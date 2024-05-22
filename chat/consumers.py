import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Message, Room

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        query_string = self.scope['query_string'].decode()
        token_key = query_string.split('=')[1] if '=' in query_string else None

        if token_key:
            user = await self.get_user_from_token(token_key)
            if user:
                self.scope['user'] = user
            else:
                await self.close()

        if self.scope['user'].is_anonymous:
            await self.close()
        else:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            logger.info(f"WebSocket connection accepted for room: {self.room_name}")

    @sync_to_async
    def get_user_from_token(self, token_key):
        try:
            token = Token.objects.get(key=token_key)
            return token.user
        except Token.DoesNotExist:
            return None

    async def disconnect(self, close_code):
        logger.info(f"Disconnected with close code: {close_code}")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            sender_username = text_data_json['sender']
            recipient_username = text_data_json['recipient']

            logger.info(f"Received message: {message} from sender: {sender_username} to recipient: {recipient_username}")

            sender = await sync_to_async(User.objects.get)(username=sender_username)
            
            if recipient_username == self.room_name:
                room, created = await sync_to_async(Room.objects.get_or_create)(name=self.room_name)
                message_instance = await sync_to_async(Message.objects.create)(sender=sender, room=room, content=message)
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message_instance.content,
                        'sender_username': sender.username,
                    }
                )
            else:
                recipient = await sync_to_async(User.objects.get)(username=recipient_username)
                message_instance = await sync_to_async(Message.objects.create)(sender=sender, recipient=recipient, content=message)
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message_instance.content,
                        'sender_username': sender.username,
                    }
                )
        except User.DoesNotExist as e:
            logger.error(f"User.DoesNotExist: {str(e)} - sender: {sender_username}, recipient: {recipient_username}")
            await self.send(text_data=json.dumps({
                'error': 'User does not exist'
            }))
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            await self.send(text_data=json.dumps({
                'error': 'Unexpected error'
            }))
            await self.close()

    async def chat_message(self, event):
        message = event['message']
        sender_username = event['sender_username']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender_username': sender_username
        }))
