# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.db import transaction
from a_users.models import Profile
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("WebSocket connection accepted in Django server")

    async def disconnect(self, close_code):
        print("WebSocket connection closed")

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            try:
                data = json.loads(text_data)
                
                message_type = data.get("type")
                if message_type == "all_users":
                    users = data.get("users", [])
                    print("Received users from Node.js server:")
                    
                    for user_data in users:
                        username = user_data.get("username")
                        email = user_data.get("email", "N/A")
                        role = user_data.get("role", "tenant") 
                        
                        # Create or update user and profile in a sync context from my node js server
                        await self.create_or_update_user_and_profile(username, email, role)

                elif "user" in data and "msg" in data:
                    print(f"Received message from {data['user']}: {data['msg']}")
                else:
                    print("Received unrecognized message type or format:", data)

            except json.JSONDecodeError:
                print("Invalid JSON format received")
            except KeyError as e:
                print(f"KeyError - Missing key in data: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")
        else:
            print("No text data received")

    @database_sync_to_async
    def create_or_update_user_and_profile(self, username, email, role):
        try:
            with transaction.atomic():
                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={"email": email}
                )
                if created:
                    user.set_password("1234")
                    user.save()
                    print(f"Created new user: {username}")

                Profile.objects.get_or_create(
                    user=user,
                    defaults={
                        "user_type": role,
                        "displayname": username,
                    }
                )
                print(f"Ensured profile for user: {username}")

        except Exception as e:
            print(f"Error creating user or profile for {username}: {e}")
