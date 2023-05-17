from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class Message(models.Model):
    sender = models.CharField(max_length=200)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.content}"


class CustomUser(AbstractUser):
    user_id = models.CharField(max_length=255, primary_key=True)

    def __str__(self):
        return self.user_id


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return str(self.phone_number)
