from django.urls import include, path, re_path

from GameApp.consumers import TicTacToeConsumer

websocket_urlpatterns = [
    re_path(r'^ws/play/(?P<room_code>\w+)/$', TicTacToeConsumer.as_asgi()),
]
