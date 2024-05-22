from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser, Message, Room
from .serializers import CustomUserSerializer, MessageSerializer, RoomSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import Q

class UserList(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class CurrentUserDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)

class MessageList(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        other_user_username = self.request.query_params.get('other_user', None)
        
        if other_user_username:
            other_user = CustomUser.objects.get(username=other_user_username)
            return Message.objects.filter(
                Q(sender=user, recipient=other_user) |
                Q(sender=other_user, recipient=user)
            ).order_by('timestamp')
        else:
            return Message.objects.filter(sender=user).order_by('timestamp')

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class UserToUserMessages(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        user = request.user
        try:
            other_user = CustomUser.objects.get(username=username)
            messages = Message.objects.filter(
                Q(sender=user, recipient=other_user) |
                Q(sender=other_user, recipient=user)
            ).order_by('timestamp')
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

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
