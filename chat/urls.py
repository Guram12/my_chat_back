# chat/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('rooms/', views.RoomList.as_view(), name='room-list'),  # Endpoint to list and create chat rooms
    path('rooms/<str:room_name>/', views.RoomDetail.as_view(), name='room-detail'),  # Endpoint for a specific chat room
]
