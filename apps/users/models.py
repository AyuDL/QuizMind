from django.contrib.auth.models import AbstractUser
from django.db import models
from common.models import UuidModel, TimestampModel
import uuid

class Users(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    league_point = models.IntegerField(default=0)
    notification_enabled = models.BooleanField(default=True)
    preferred_category = models.ManyToManyField('quizzs.Category', blank = True)        #To store the preferred category of the user
    accepted_terms = models.BooleanField(default=False)                                 #To store whether the user has accepted the terms and conditions

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class Badges(UuidModel, models):
    title = models.CharField(max_length=100, unique=True)
    content = models.TextField()
    condition_target = models.IntegerField()

    class Meta:
        db_table = 'badges'
        verbose_name = 'Badge'
        verbose_name_plural = 'Badges'

class User_badge(UuidModel, TimestampModel):
    progress = models.IntegerField(default=0)
    badge_id = models.ForeignKey(Badges, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_badge'
        verbose_name = 'User Badge'
        verbose_name_plural = 'User Badges'