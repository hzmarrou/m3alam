from django.conf import settings
from django.db import models


class JobRequest(models.Model):
    class Status(models.TextChoices):
        OPEN = "open", "Ouverte"
        ASSIGNED = "assigned", "Attribuée"
        CLOSED = "closed", "Fermée"
        HIDDEN = "hidden", "Masquée"

    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="jobs")
    category = models.CharField(max_length=80)
    title = models.CharField(max_length=120)
    description = models.TextField()
    city = models.CharField(max_length=120)
    budget_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    budget_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.title
