from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from common.models import UuidModel, TimestampModel
import uuid

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("email address"), unique=True, max_length=255)          #Overload attribut to set them with blank = False
    first_name = models.CharField(_("first name"), max_length=150)                      #Overload attribut to set them with blank = False
    last_name = models.CharField(_("last name"), max_length=150)                        #Overload attribut to set them with blank = False
    is_active = models.BooleanField(_("active"), default=False,
            help_text=_(
                "Designates whether this user should be treated as active. "
                "Unselect this instead of deleting accounts."
            )),                                                                          #Overload attribut to set them with default = False
    league_point = models.IntegerField(default=0)
    notification_enabled = models.BooleanField(default=True)
    preferred_category = models.ManyToManyField('quizzs.Category', blank = True, related_name="preferred_by")         #To store the preferred category of the user

class Badge(UuidModel):
    title = models.CharField(max_length=100, unique=True)
    content = models.TextField()
    condition_target = models.IntegerField()

class User_badge(UuidModel, TimestampModel):
    progress = models.IntegerField(default=0)
    badge_id = models.ForeignKey(Badge, on_delete=models.CASCADE)

class TokenPurpose(models.TextChoices):
    ACCOUNT_VALIDATION = "account_validation", "Validation de compte"
    PASSWORD_RESET = "password_reset", "Réinitialisation mot de passe"

class Token(UuidModel, TimestampModel):
    value = models.CharField(max_length=255, unique=True)
    purpose = models.CharField(max_length=30, choices=TokenPurpose.choices)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="tokens")
    expires_at = models.DateTimeField()
    used = models.DateTimeField(null=True, blank=True)

    def is_valid(self):
        return self.used_at is None and timezone.now() < self.expires_at