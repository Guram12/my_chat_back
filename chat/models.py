from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    bio = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(null=True, blank=True)

    
    def __str__(self):
        return self.username

class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    participants = models.ManyToManyField(CustomUser, related_name='rooms')

    def __str__(self):
        return self.name

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(CustomUser, related_name='received_messages', null=True, blank=True, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='messages', null=True, blank=True, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.recipient:
            return f"{self.sender} to {self.recipient}: {self.content}"
        else:
            return f"{self.sender} to room {self.room.name}: {self.content}"
