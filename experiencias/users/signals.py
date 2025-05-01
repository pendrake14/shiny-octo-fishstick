from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import User


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create a user profile when a new user is created.
    """
    if created:
        # Create any additional user-related objects here if needed
        pass 