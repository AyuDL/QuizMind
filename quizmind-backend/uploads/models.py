from apps.common.models import UuidModel, TimestampModel
from django.db import models

class UploadedFile(UuidModel, TimestampModel):
    url = models.CharField()
    file_full_name = models.CharField()
    file_custom_name = models.CharField()
