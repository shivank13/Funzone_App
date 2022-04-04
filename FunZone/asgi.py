import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import GameApp.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FunZone.settings')



# application = get_asgi_application()
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            GameApp.routing.websocket_urlpatterns
        )
    ),
})
