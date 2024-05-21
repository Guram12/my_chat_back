from rest_framework import generics, permissions
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Message, Room
from .serializers import UserSerializer, MessageSerializer, RoomSerializer
from rest_framework.permissions import IsAuthenticated

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CurrentUserDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    
class MessageList(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(sender=user) | Message.objects.filter(recipient=user)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class RoomList(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        room = serializer.save()
        room.participants.add(self.request.user)

class RoomDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

class RoomMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, room_name):
        try:
            room = Room.objects.get(name=room_name)
            messages = Message.objects.filter(room=room).order_by('timestamp')
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data)
        except Room.DoesNotExist:
            return Response({"error": "Room not found"}, status=404)




@api_view(['POST'])
def logout(request):
    request.user.auth_token.delete()
    return Response(status=status.HTTP_200_OK)
