# chat/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class RoomList(APIView):
    def get(self, request):
        # Here you would list all chat rooms
        rooms = [{"name": "room1"}, {"name": "room2"}]  # Example data
        return Response(rooms)

    def post(self, request):
        # Here you would create a new chat room
        room_name = request.data.get('name')
        if room_name:
            # Code to create a new room
            return Response({"message": f"Room '{room_name}' created"}, status=status.HTTP_201_CREATED)
        return Response({"error": "Room name is required"}, status=status.HTTP_400_BAD_REQUEST)

class RoomDetail(APIView):
    def get(self, request, room_name):
        # Here you would get details of a specific chat room
        return Response({"name": room_name, "messages": []})  # Example data

    def delete(self, request, room_name):
        # Here you would delete a chat room
        return Response({"message": f"Room '{room_name}' deleted"}, status=status.HTTP_204_NO_CONTENT)
