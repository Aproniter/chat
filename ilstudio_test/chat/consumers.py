import json

from django.contrib.auth import get_user_model
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from .models import Chat, Message


User = get_user_model()

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.chat_title = self.scope['url_route']['kwargs']['chat_title']
        self.chat_group_title = "chat_%s" % self.chat_title
        async_to_sync(self.channel_layer.group_add)(
            self.chat_group_title, self.channel_name
        )
        self.chat, created = Chat.objects.get_or_create(title=self.chat_title)
        self.user = self.scope['user']
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_group_title, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        text = text_data_json['message']
        message = Message.objects.create(
            chat=self.chat,
            author=self.user,
            text=text
        )
        async_to_sync(self.channel_layer.group_send)(
            self.chat_group_title, {
                'type': 'chat_message',
                'message': json.dumps({
                    'id': message.id,
                    'text': message.text,
                    'author': message.author.username,
                    'created_at': message.created_at.strftime("%m-%d-%Y %H:%M:%S"),
                    'chat': message.chat.title,
                })
            }
        )

    def chat_message(self, event):
        text = event['message']
        self.send(text_data=text)
