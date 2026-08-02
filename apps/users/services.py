from datetime import timedelta
from.models import Token
from django.utils import timezone
import secrets

def create_token(user, purpose, lifetime_minutes=5):
    return Token.objects.create(
        user=user,
        purpose=purpose,
        value=secrets.token_urlsafe(32),
        expires_at=timezone.now() + timedelta(minutes=lifetime_minutes),
    )

def consume_token(value, purpose):
    try:
        token = Token.objects.get(value=value, purpose=purpose)
    except Token.DoesNotExist:
        return None

    if not token.is_valid():
        return None

    token.used_at = timezone.now()
    token.save()
    return token.user