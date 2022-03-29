from django.urls import path
from .views import *

urlpatterns = [
    path('tictactoe', home, name='home'),
    path('play/<room_code>', play, name='play'),

]
