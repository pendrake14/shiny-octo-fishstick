from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserTypeChoices(models.TextChoices):
    GUEST = "GUEST"
    HOST = "HOST"


class User(AbstractUser):
    """
    Custom User model that extends Django's AbstractUser.
    """

    email = models.EmailField(_("email address"), unique=True)
    is_verified = models.BooleanField(_("verified"), default=False)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    user_type = models.CharField(
        max_length=10, choices=UserTypeChoices.choices, default=UserTypeChoices.GUEST
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["-created_at"]

    def __str__(self):
        return self.email
    
class UserProfile(models.Model):
    user = models.OneToOneField(
        'User',
        on_delete=models.CASCADE,
        related_name='profile'
    )

    phone_number = models.CharField(_("phone number"), max_length=15, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    # HOST
    company_name = models.CharField(max_length=255, blank=True)
    website = models.URLField(blank=True)

    # GUEST
    favorite_categories = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"
