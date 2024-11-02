
```markdown
# Django Chat Application

This is a Django-based chat application that Django Channels for real-time WebSocket communication.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Running the Server](#running-the-server)
- [API Endpoints](#api-endpoints)
  - [HTTP Endpoints](#http-endpoints)
  - [WebSocket Endpoints](#websocket-endpoints)
- [Functions](#functions)

## Features

- Real-time messaging through WebSocket connections.
- Private and public chatrooms.
- User authentication and authorization.
- Online user count display.
- New message notification system.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/godfrey-tankan/serice-django.git
   cd service-django
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. **Install required packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the PostgreSQL database:**

   Make sure you have PostgreSQL installed. Update your `settings.py` file to include your database configuration.

   Install the required database packages:

   ```bash
   pip install dj-database-url psycopg2-binary
   ```

5. **Set up environment variables:**

   Create a `.env` file in the root directory of your project and configure the required settings such as `DATABASE_URL`, `SECRET_KEY`, and `DEBUG`.

6. **Migrate the database:**

   ```bash
   python manage.py migrate
   ```

7. **Create a superuser (optional):**

   ```bash
   python manage.py createsuperuser
   ```

## Running the Server

To start the server, use Daphne to run the ASGI application:

```bash
daphne a_core.asgi:application -b 0.0.0.0 -p 8000
```

## API Endpoints

### HTTP Endpoints

1. **Profiles View**
   - **URL:** `/`
   - **Method:** GET
   - **Description:** Displays the profiles page.

2. **Profiles View (Alias)**
   - **URL:** `/profiles/`
   - **Method:** GET
   - **Description:** Displays the profiles page.

3. **Start Chat**
   - **URL:** `/chat/<user_name>/`
   - **Method:** GET
   - **Description:** Starts a chatroom with the specified user. Redirects to the chatroom if it exists or creates a new one.

4. **Chatroom**
   - **URL:** `/chat/room/<chatroom_name>/send/`
   - **Method:** GET
   - **Description:** Handles chat message sending and rendering the chatroom interface.

### WebSocket Endpoints

1. **Chat Room WebSocket**
   - **URL:** `ws/chatroom/<chatroom_name>/`
   - **Description:** Connects to a specific chatroom for real-time messaging.

2. **Chat WebSocket**
   - **URL:** `ws/chat/`
   - **Description:** General WebSocket connection for other chat functionalities.

## Functions

### Chat View
```python
@login_required
def chat_view(request, chatroom_name='public-chat'):
    ...
```
- Handles the chat interface rendering, message submission, and user role management.

### Get or Create Chatroom
```python
def get_object_or_create_chatroom(request, user_name):
    ...
```
- Retrieves or creates a private chatroom between two users.

### Chat Room Consumer
```python
class ChatRoomConsumer(WebsocketConsumer):
    ...
```
- Manages WebSocket connections for chatrooms, including message reception and broadcasting.

### Chat Consumer
```python
class ChatConsumer(AsyncWebsocketConsumer):
    ...
```
- General WebSocket consumer for handling messages sent over WebSocket.

## Additional Commands

- **Install Environment Variables**: `pip install django-environ`
- **Toggle Debug Mode**: Adjust `DEBUG` in your `.env` file.
- **Run the Application**: Follow the steps in the "Running the Server" section to start the server.


