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


class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []