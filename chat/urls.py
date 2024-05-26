from django.urls import path
from .views import UserList, UserDetail, MessageList, RoomList, RoomDetail, RoomMessagesView \
    ,logout , CurrentUserDetail, UserToUserMessages , heartbeat
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('users/me/', CurrentUserDetail.as_view(), name='user-detail'),
    path('messages/', MessageList.as_view(), name='message-list'),
    path('messages/<str:username>/', UserToUserMessages.as_view(), name='user-to-user-messages'),
    path('rooms/', RoomList.as_view(), name='room-list'),
    path('rooms/<int:pk>/', RoomDetail.as_view(), name='room-detail'),
    path('login/', obtain_auth_token, name='login'),
    path('logout/', logout, name='logout'),
    path('rooms/<str:room_name>/messages/', RoomMessagesView.as_view(), name='room-messages'),
    path('heartbeat/', heartbeat, name='heartbeat'),

]
