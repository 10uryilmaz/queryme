from django.db import models

class UploadedData(models.Model):
    data = models.JSONField()
    table_name = models.CharField(max_length=200, default='df')
