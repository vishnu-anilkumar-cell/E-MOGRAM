# User/routing.py
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/some_url/', consumers.MyConsumer.as_asgi()),  # Use your consumer class
]
