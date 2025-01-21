from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)  # This will automatically set the timestamp when the message is created.

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}: {self.content}"
