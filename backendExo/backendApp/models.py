from django.db import models
from django.contrib.auth.models import AbstractUser


class LogUpload(models.Model):
    # uploadedFile_path = models.FileField(upload_to='log_uploads/')
    uploadedFile_path = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateField()


class ForwarderData(models.Model):
    file_name = models.CharField(max_length=255)
    log_data = models.TextField()
    received_at = models.DateTimeField(auto_now_add=True)
    email = models.CharField(max_length=255)
    indexed_datetime = models.DateTimeField(auto_now_add=True)  # Add indexed_datetime field
    isForwarder = models.BooleanField(default=False)
    host = models.CharField(max_length=255)

class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class APIKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=255)
    key_name = models.CharField(max_length=255)
    is_forwarder = models.BooleanField(default=False)
