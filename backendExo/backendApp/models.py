from django.db import models


class LogUpload(models.Model):
    # uploadedFile_path = models.FileField(upload_to='log_uploads/')
    uploadedFile_path = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateField()

class ForwarderData(models.Model):
    file_name = models.CharField(max_length=255)
    log_data = models.TextField()
    received_at = models.DateTimeField(auto_now_add=True)

