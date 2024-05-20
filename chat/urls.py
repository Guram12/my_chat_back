from django.urls import path
from .views import UserList, UserDetail, MessageList, RoomList, RoomDetail, RoomMessages, logout
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('messages/', MessageList.as_view(), name='message-list'),
    path('rooms/', RoomList.as_view(), name='room-list'),
    path('rooms/<int:pk>/', RoomDetail.as_view(), name='room-detail'),
    path('rooms/<int:room_id>/messages/', RoomMessages.as_view(), name='room-messages'),
    path('login/', obtain_auth_token, name='login'),
    path('logout/', logout, name='logout'),
]
