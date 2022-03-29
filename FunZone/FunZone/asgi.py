import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from GameApp.consumers import GameRoom
from django.core.asgi import get_asgi_application
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FunZone.settings')

application = get_asgi_application()

ws_pattern = [
    path('ws/game/<room_code>', GameRoom)
]

application = ProtocolTypeRouter(
    {
        'websocket': AuthMiddlewareStack(URLRouter(
            ws_pattern
        ))
    }
)
