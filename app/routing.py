from django.urls import path
from . import consumers

websocket_urlpatterns=[
    path('ws/chatting_to/<str:room_name>/', consumers.YourConsumer.as_asgi())
]
