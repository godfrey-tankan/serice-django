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

