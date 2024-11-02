from django.urls import path
from .consumers import *
from .server import *

websocket_urlpatterns = [
    path("ws/chatroom/<chatroom_name>/", ChatRoomConsumer.as_asgi()),
    path("ws/room/<chatroom_name>/", ChatRoomsConsumer.as_asgi()),
    path('ws/chat/',ChatConsumer.as_asgi()), 
]