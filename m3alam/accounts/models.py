from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        CLIENT = "client", "Client"
        ARTISAN = "artisan", "Artisan"
        ADMIN = "admin", "Admin"

    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CLIENT)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return f"{self.email} ({self.get_role_display()})"


class ArtisanProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="artisan_profile")
    full_name = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    skills = models.CharField(max_length=255, help_text="Séparez par virgule")
    bio = models.TextField(blank=True)
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.full_name
