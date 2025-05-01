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