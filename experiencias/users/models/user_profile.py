from django.db import models
from django.utils.translation import gettext_lazy as _

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
