#File to handle uuid method to set all classes uuid.
from django.db import models
import uuid

class UuidModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)         #No use about self here because it's class attribute.

class TimestampModel(models.Model):
      created_at = models.DateTimeField(auto_now_add=True)

class Meta:                                                                             #Class Meta drive Django to understand how use the class
        abstract = True