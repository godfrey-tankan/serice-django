from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json
from .models import *
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from asgiref.sync import async_to_sync
from django.db.models import Count


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))



class ChatRoomsConsumer(WebsocketConsumer):
    chats = GroupMessage.objects.all().delete()
    def connect(self):
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        try:
            self.chatroom = ChatGroup.objects.get(group_name=self.chatroom_name)
        except Exception:
            self.get_user_by_name()
        if not self.chatroom:
            print('Chatroom not found....................')
            self.get_user_by_name()
        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name,
            self.channel_name
        )
        self.accept()

        if self.user not in self.chatroom.users_online.all():
            self.chatroom.users_online.add(self.user)
            self.update_online_users_count()

    def get_user_by_name(self):
        self.users = self.channel_name.split('_')
        self.sender = self.users[0]
        self.receiver = self.users[1]
        user1 = User.objects.get_or_create(username=self.sender)
        user2 = User.objects.get_or_create(username=self.receiver)
        chat_groups = ChatGroup.objects.filter(
            members__in=[user1, user2] 
        ).annotate(
            member_count=Count('members') 
        ).filter(
            member_count__gte=2 
        ).first()
        if chat_groups.exists():
            print('Chat group exists....', chat_groups)
            self.chatroom = chat_groups
        else:
            print('Creating new chat group....')
            self.chatroom = ChatGroup.objects.create(group_name=self.chatroom_name)
    
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name,
            self.channel_name
        )
        if self.user in self.chatroom.users_online.all():
            self.chatroom.users_online.remove(self.user)
            self.update_online_users_count()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json['body']
        message = GroupMessage.objects.create(
            group=self.chatroom,
            author=self.user, 
            body=body,
        )
        self.send_new_message_count()
        
        event = {
            'type': 'message_handler',
            'message_id': message.id,
        }

        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )
        
    def message_handler(self, event):
        message_id = event['message_id']
        message = GroupMessage.objects.get(id=message_id)
        context = {'message': message, 'user': self.user}
        html = render_to_string('a_rtchat/partials/chat_message_p.html', context=context)
        self.send(text_data=html)

    def update_online_users_count(self):
        event = {
            'type': 'online_users_count',
            'count': self.chatroom.users_online.count() - 1,
        }
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )

    def online_users_count(self, event):
        count = event['count']
        html = render_to_string('a_rtchat/partials/online_count.html', {'online_count': count})
        self.send(text_data=html)

    def send_new_message_count(self):
        count = GroupMessage.objects.filter(group=self.chatroom, is_read=False).count()
        print('COUNTED.... messages:', count)
        event = {
            'type': 'new_message_count',
            'count': count,
        }
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )
    
    def new_message_count(self, event):
        count = event['count']
        html = render_to_string('a_rtchat/partials/new_message_count.html', {'new_message_count': count})
        self.send(text_data=html)
